#!/bin/bash

#
# Framework Template Validation Test Suite
#
# DESCRIPTION:
#   Validates the integrity and completeness of Scratchpad framework templates.
#   Tests for file existence, content validation, and structural consistency
#   across all framework variants in the repository.
#
# USAGE:
#   ./test_framework_templates.sh
#
# REQUIREMENTS:
#   - Bash shell environment
#   - grep, wc, and file commands
#
# EXIT CODES:
#   0 - All templates valid
#   1 - One or more template issues found
#

set -euo pipefail

# Test configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"
TEST_COUNT=0
PASS_COUNT=0
FAIL_COUNT=0

# Function: log_test_result
# Description: Logs and tracks test results with detailed output
# Parameters:
#   $1 - Test name
#   $2 - Result (0=pass, 1=fail)
#   $3 - Optional details
# Returns: Updates global counters
log_test_result() {
    local test_name="$1"
    local result="$2"
    local details="${3:-}"
    
    TEST_COUNT=$((TEST_COUNT + 1))
    echo -n "Test $TEST_COUNT: $test_name ... "
    
    if [ "$result" -eq 0 ]; then
        echo "PASS"
        PASS_COUNT=$((PASS_COUNT + 1))
    else
        echo "FAIL"
        [ -n "$details" ] && echo "  Details: $details"
        FAIL_COUNT=$((FAIL_COUNT + 1))
    fi
}

# Function: test_core_frameworks_exist
# Description: Validates that all core framework files referenced in README exist
# Parameters: None
# Returns: 0 if all core frameworks exist, 1 if any missing
test_core_frameworks_exist() {
    local missing_files=()
    
    # Core framework files from README
    local core_files=(
        "2.5-refined-040125.md"
        "2.5-medium-071825.md"
        "scratchpad-lite-071625.md"
        "scratchpad-think_v4_1208.txt"
        "pplx-AI-profile-cplx-1-update.txt"
    )
    
    for file in "${core_files[@]}"; do
        if [ ! -f "$BASE_DIR/$file" ]; then
            missing_files+=("$file")
        fi
    done
    
    if [ ${#missing_files[@]} -eq 0 ]; then
        log_test_result "Core framework files exist" 0
        return 0
    else
        local details="Missing: ${missing_files[*]}"
        log_test_result "Core framework files exist" 1 "$details"
        return 1
    fi
}

# Function: test_purpose_built_frameworks_exist
# Description: Validates that all purpose-built framework files exist
# Parameters: None
# Returns: 0 if all purpose-built frameworks exist, 1 if any missing
test_purpose_built_frameworks_exist() {
    local missing_files=()
    
    # Purpose-built framework files from README
    local purpose_built_files=(
        "purpose-built/G.A.B.G-Phased App-Game Design.txt"
        "purpose-built/deeper_research_040125.md"
        "purpose-built/gemini-cli-scratchpad-071625.md"
        "purpose-built/novelize_output_review_GPT-5-080825.txt"
        "purpose-built/Human Condition Benchmark.md"
        "purpose-built/Sonnet 3.7 Thinking.md"
        "purpose-built/saganpad_072525.md"
        "purpose-built/Unified Conscious Embodiment.md"
    )
    
    for file in "${purpose_built_files[@]}"; do
        if [ ! -f "$BASE_DIR/$file" ]; then
            missing_files+=("$file")
        fi
    done
    
    if [ ${#missing_files[@]} -eq 0 ]; then
        log_test_result "Purpose-built frameworks exist" 0
        return 0
    else
        local details="Missing: ${missing_files[*]}"
        log_test_result "Purpose-built frameworks exist" 1 "$details"
        return 1
    fi
}

# Function: test_frameworks_not_empty
# Description: Validates that framework files have meaningful content (>100 bytes)
# Parameters: None
# Returns: 0 if all frameworks have content, 1 if any are too small
test_frameworks_not_empty() {
    local small_files=()
    local min_size=100  # Minimum size in bytes
    
    # Check all markdown and text framework files
    while IFS= read -r -d '' file; do
        local size
        size=$(stat -c%s "$file" 2>/dev/null || echo 0)
        
        if [ "$size" -lt $min_size ]; then
            local rel_path="${file#$BASE_DIR/}"
            small_files+=("$rel_path ($size bytes)")
        fi
    done < <(find "$BASE_DIR" -name "*.md" -o -name "*.txt" | grep -E "(scratchpad|framework)" | head -20 | tr '\n' '\0')
    
    if [ ${#small_files[@]} -eq 0 ]; then
        log_test_result "Frameworks have adequate content" 0
        return 0
    else
        local details="Small files: ${small_files[*]}"
        log_test_result "Frameworks have adequate content" 1 "$details"
        return 1
    fi
}

# Function: test_license_file_exists
# Description: Validates that the license file exists and has content
# Parameters: None
# Returns: 0 if license exists and has content, 1 otherwise
test_license_file_exists() {
    local license_file="$BASE_DIR/license.txt"
    
    if [ ! -f "$license_file" ]; then
        log_test_result "License file exists" 1 "license.txt not found"
        return 1
    fi
    
    if [ ! -s "$license_file" ]; then
        log_test_result "License file exists" 1 "license.txt is empty"
        return 1
    fi
    
    # Check for MIT license content
    if ! grep -qi "MIT" "$license_file"; then
        log_test_result "License file exists" 1 "Does not contain MIT license text"
        return 1
    fi
    
    log_test_result "License file exists and contains MIT license" 0
    return 0
}

# Function: test_old_versions_directory
# Description: Validates that _oldversions directory exists and contains files
# Parameters: None
# Returns: 0 if directory exists with content, 1 otherwise
test_old_versions_directory() {
    local old_versions_dir="$BASE_DIR/_oldversions"
    
    if [ ! -d "$old_versions_dir" ]; then
        log_test_result "_oldversions directory exists" 1 "Directory not found"
        return 1
    fi
    
    local file_count
    file_count=$(find "$old_versions_dir" -type f | wc -l)
    
    if [ "$file_count" -eq 0 ]; then
        log_test_result "_oldversions contains files" 1 "Directory is empty"
        return 1
    fi
    
    log_test_result "_oldversions directory exists with $file_count files" 0
    return 0
}

# Function: test_showcase_directory_integrity
# Description: Validates showcase directory has expected media files
# Parameters: None
# Returns: 0 if showcase has adequate content, 1 otherwise
test_showcase_directory_integrity() {
    local showcase_dir="$BASE_DIR/showcase"
    
    if [ ! -d "$showcase_dir" ]; then
        log_test_result "Showcase directory exists" 1 "Directory not found"
        return 1
    fi
    
    # Count different types of media files
    local png_count gif_count
    png_count=$(find "$showcase_dir" -name "*.png" | wc -l)
    gif_count=$(find "$showcase_dir" -name "*.gif" | wc -l)
    
    local total_media=$((png_count + gif_count))
    
    if [ "$total_media" -lt 5 ]; then
        log_test_result "Showcase has adequate media" 1 "Only $total_media media files found"
        return 1
    fi
    
    log_test_result "Showcase directory has $total_media media files" 0
    return 0
}

# Function: print_summary
# Description: Prints comprehensive test results and statistics
# Parameters: None
# Returns: 0 if all tests passed, 1 if any failed
print_summary() {
    echo
    echo "=== Framework Template Validation Summary ==="
    echo "Total Tests: $TEST_COUNT"
    echo "Passed:      $PASS_COUNT"
    echo "Failed:      $FAIL_COUNT"
    echo
    
    if [ $FAIL_COUNT -eq 0 ]; then
        echo "All framework validation tests PASSED! ✓"
        return 0
    else
        echo "Some framework validation tests FAILED! ✗"
        echo "Please review and fix the identified issues."
        return 1
    fi
}

# Main test execution
main() {
    echo "=== Framework Template Validation Test Suite ==="
    echo "Base directory: $BASE_DIR"
    echo
    
    cd "$BASE_DIR" || {
        echo "ERROR: Cannot change to base directory"
        exit 1
    }
    
    # Execute all test cases
    test_core_frameworks_exist
    test_purpose_built_frameworks_exist
    test_frameworks_not_empty
    test_license_file_exists
    test_old_versions_directory
    test_showcase_directory_integrity
    
    # Print results and exit
    print_summary
}

# Execute main function if script is run directly
if [ "${BASH_SOURCE[0]}" == "${0}" ]; then
    main "$@"
fi