#!/bin/bash

#
# Bug Fix Validation Test Suite
#
# DESCRIPTION:
#   Validates that the specific bugs identified and fixed in this repository
#   are actually resolved. This test suite serves as regression testing to
#   ensure the fixes work correctly and prevent future regressions.
#
# USAGE:
#   ./test_bug_fixes.sh
#
# BUGS TESTED:
#   1. Major Bug: Broken showcase file references in README.md
#   2. Minor Bug 1: remedial.sh references non-existent remedial_v2.sh
#   3. Minor Bug 2: remedial.sh hardcoded /app directory path
#   4. Minor Bug 3: Empty corrupted gif file in root directory
#   5. Minor Bug 4: Filename typo "protocal" instead of "protocol"
#
# EXIT CODES:
#   0 - All bug fixes verified
#   1 - One or more bugs still present or fixes broken
#

set -euo pipefail

# Test configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"
TEST_COUNT=0
PASS_COUNT=0
FAIL_COUNT=0

# Function: log_test_result
# Description: Logs and tracks bug fix test results
# Parameters:
#   $1 - Bug test name
#   $2 - Result (0=fixed, 1=still broken)
#   $3 - Optional details
# Returns: Updates global counters
log_test_result() {
    local test_name="$1"
    local result="$2"
    local details="${3:-}"
    
    TEST_COUNT=$((TEST_COUNT + 1))
    echo -n "Bug Fix Test $TEST_COUNT: $test_name ... "
    
    if [ "$result" -eq 0 ]; then
        echo "FIXED ✓"
        PASS_COUNT=$((PASS_COUNT + 1))
    else
        echo "BROKEN ✗"
        [ -n "$details" ] && echo "  Details: $details"
        FAIL_COUNT=$((FAIL_COUNT + 1))
    fi
}

# Function: test_showcase_file_references_fixed
# Description: Validates that showcase file references in README now work
# Parameters: None
# Returns: 0 if all showcase files exist, 1 if any missing
test_showcase_file_references_fixed() {
    local readme_file="$BASE_DIR/README.md"
    local missing_files=()
    
    # The specific files that were broken and should now work
    local showcase_files=(
        "showcase/4 images.png"
        "showcase/scratchpad from main_new.gif"
        "showcase/create scratchpad collection.gif"
        "showcase/TLDR Task with Canvas.png"
    )
    
    for file in "${showcase_files[@]}"; do
        if [ ! -f "$BASE_DIR/$file" ]; then
            missing_files+=("$file")
        fi
    done
    
    if [ ${#missing_files[@]} -eq 0 ]; then
        log_test_result "Major Bug - Showcase file references" 0
        return 0
    else
        local details="Still missing: ${missing_files[*]}"
        log_test_result "Major Bug - Showcase file references" 1 "$details"
        return 1
    fi
}

# Function: test_remedial_script_no_longer_references_v2
# Description: Validates that remedial.sh no longer references non-existent remedial_v2.sh
# Parameters: None
# Returns: 0 if reference removed, 1 if still present
test_remedial_script_no_longer_references_v2() {
    local remedial_script="$BASE_DIR/jules-kit/scripts/remedial.sh"
    
    if [ ! -f "$remedial_script" ]; then
        log_test_result "Minor Bug 1 - remedial_v2.sh reference" 1 "remedial.sh not found"
        return 1
    fi
    
    if grep -q "remedial_v2.sh" "$remedial_script"; then
        log_test_result "Minor Bug 1 - remedial_v2.sh reference" 1 "Still references remedial_v2.sh"
        return 1
    fi
    
    log_test_result "Minor Bug 1 - remedial_v2.sh reference removed" 0
    return 0
}

# Function: test_remedial_script_no_hardcoded_app_path
# Description: Validates that remedial.sh no longer uses hardcoded /app path
# Parameters: None
# Returns: 0 if hardcoded path removed, 1 if still present
test_remedial_script_no_hardcoded_app_path() {
    local remedial_script="$BASE_DIR/jules-kit/scripts/remedial.sh"
    
    if [ ! -f "$remedial_script" ]; then
        log_test_result "Minor Bug 2 - hardcoded /app path" 1 "remedial.sh not found"
        return 1
    fi
    
    if grep -q "cd /app" "$remedial_script"; then
        log_test_result "Minor Bug 2 - hardcoded /app path" 1 "Still contains 'cd /app'"
        return 1
    fi
    
    # Should now use dynamic path detection
    if ! grep -q 'cd "$base_dir"' "$remedial_script"; then
        log_test_result "Minor Bug 2 - hardcoded /app path" 1 "Dynamic path not implemented"
        return 1
    fi
    
    log_test_result "Minor Bug 2 - hardcoded /app path replaced with dynamic" 0
    return 0
}

# Function: test_empty_gif_file_removed
# Description: Validates that the corrupted empty gif file was removed
# Parameters: None
# Returns: 0 if empty file removed, 1 if still present
test_empty_gif_file_removed() {
    local empty_gif="$BASE_DIR/scratchpad-from-main_new.gif"
    
    if [ -f "$empty_gif" ]; then
        local size
        size=$(stat -c%s "$empty_gif" 2>/dev/null || echo 0)
        
        if [ "$size" -eq 0 ]; then
            log_test_result "Minor Bug 3 - empty gif file" 1 "Empty gif file still present"
            return 1
        fi
    fi
    
    log_test_result "Minor Bug 3 - empty gif file removed" 0
    return 0
}

# Function: test_filename_typo_fixed
# Description: Validates that "protocal" typo was fixed to "protocol"
# Parameters: None
# Returns: 0 if typo fixed, 1 if still present
test_filename_typo_fixed() {
    local typo_file="$BASE_DIR/showcase/thinking_scratchpad_protocal.gif"
    local correct_file="$BASE_DIR/showcase/thinking_scratchpad_protocol.gif"
    
    if [ -f "$typo_file" ]; then
        log_test_result "Minor Bug 4 - filename typo 'protocal'" 1 "Typo file still exists"
        return 1
    fi
    
    if [ ! -f "$correct_file" ]; then
        log_test_result "Minor Bug 4 - filename typo 'protocal'" 1 "Corrected file not found"
        return 1
    fi
    
    log_test_result "Minor Bug 4 - filename typo fixed to 'protocol'" 0
    return 0
}

# Function: test_remedial_script_functionality
# Description: Validates that the fixed remedial script actually works
# Parameters: None
# Returns: 0 if script executes successfully, 1 if broken
test_remedial_script_functionality() {
    local remedial_script="$BASE_DIR/jules-kit/scripts/remedial.sh"
    local temp_dir
    temp_dir=$(mktemp -d)
    
    cd "$temp_dir" || return 1
    
    # Test script execution in a clean environment
    if timeout 30 bash "$remedial_script" >/dev/null 2>&1; then
        cd - >/dev/null || true
        rm -rf "$temp_dir"
        log_test_result "Remedial script functionality after fixes" 0
        return 0
    else
        cd - >/dev/null || true
        rm -rf "$temp_dir"
        log_test_result "Remedial script functionality after fixes" 1 "Script fails to execute"
        return 1
    fi
}

# Function: print_bug_fix_summary
# Description: Prints comprehensive bug fix validation results
# Parameters: None
# Returns: 0 if all bugs fixed, 1 if any still present
print_bug_fix_summary() {
    echo
    echo "=== Bug Fix Validation Summary ==="
    echo "Total Bug Tests: $TEST_COUNT"
    echo "Bugs Fixed:      $PASS_COUNT"
    echo "Still Broken:    $FAIL_COUNT"
    echo
    
    if [ $FAIL_COUNT -eq 0 ]; then
        echo "🐛➜✅ ALL IDENTIFIED BUGS HAVE BEEN FIXED! 🐛➜✅"
        echo
        echo "Verification complete:"
        echo "  ✓ Major showcase file reference bug resolved"
        echo "  ✓ Shell script reference issues fixed"
        echo "  ✓ Hardcoded path problems corrected"
        echo "  ✓ Corrupted files cleaned up"
        echo "  ✓ Filename typos corrected"
        echo "  ✓ All fixes maintain functionality"
        echo
        return 0
    else
        echo "⚠️  $FAIL_COUNT BUG(S) STILL PRESENT OR FIXES BROKEN ⚠️"
        echo
        echo "Please review the failed tests and ensure fixes are correct."
        return 1
    fi
}

# Main test execution
main() {
    echo "=== Bug Fix Validation Test Suite ==="
    echo "Base directory: $BASE_DIR"
    echo "Validating that identified bugs have been properly fixed..."
    echo
    
    cd "$BASE_DIR" || {
        echo "ERROR: Cannot change to base directory"
        exit 1
    }
    
    # Execute bug fix validation tests
    test_showcase_file_references_fixed
    test_remedial_script_no_longer_references_v2
    test_remedial_script_no_hardcoded_app_path
    test_empty_gif_file_removed
    test_filename_typo_fixed
    test_remedial_script_functionality
    
    # Print results and exit
    print_bug_fix_summary
}

# Execute main function if script is run directly
if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
    main "$@"
fi