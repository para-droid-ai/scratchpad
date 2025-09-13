#!/bin/bash

#
# Markdown Link Validation Test Suite
#
# DESCRIPTION:
#   Comprehensive test suite for validating all internal file references
#   in markdown files throughout the repository. Tests for broken links,
#   missing files, and malformed references.
#
# USAGE:
#   ./test_markdown_links.sh
#
# REQUIREMENTS:
#   - Bash shell environment  
#   - grep command for pattern matching
#
# EXIT CODES:
#   0 - All links valid
#   1 - One or more broken links found
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

# Function: test_readme_framework_links
# Description: Validates all framework file references in README.md
# Parameters: None
# Returns: 0 if all links valid, 1 if any broken
test_readme_framework_links() {
    local readme_file="$BASE_DIR/README.md"
    local failed_files=()
    
    if [ ! -f "$readme_file" ]; then
        log_test_result "README.md exists" 1 "README.md not found"
        return 1
    fi
    
    # Extract markdown links and test each file reference
    while IFS= read -r line; do
        # Look for .md and .txt files in markdown links
        if echo "$line" | grep -q '\[.*\](.*\.md)' || echo "$line" | grep -q '\[.*\](.*\.txt)'; then
            # Extract the file path using sed
            local file_ref
            file_ref=$(echo "$line" | sed -n 's/.*\[\([^]]*\)\](\([^)]*\.\(md\|txt\)\)).*/\2/p' | head -1)
            
            if [ -n "$file_ref" ]; then
                # URL decode the path
                file_ref=$(echo "$file_ref" | sed 's/%20/ /g')
                local full_path="$BASE_DIR/$file_ref"
                if [ ! -f "$full_path" ]; then
                    failed_files+=("$file_ref")
                fi
            fi
        fi
    done < "$readme_file"
    
    if [ ${#failed_files[@]} -eq 0 ]; then
        log_test_result "README framework file references" 0
        return 0
    else
        local details="Missing files: ${failed_files[*]}"
        log_test_result "README framework file references" 1 "$details"
        return 1
    fi
}

# Function: test_readme_showcase_links  
# Description: Validates all showcase file references in README.md
# Parameters: None
# Returns: 0 if all links valid, 1 if any broken
test_readme_showcase_links() {
    local readme_file="$BASE_DIR/README.md"
    local failed_files=()
    
    # Test showcase file references specifically
    while IFS= read -r line; do
        if echo "$line" | grep -q '\[.*\](showcase/'; then
            # Extract showcase file path
            local file_ref
            file_ref=$(echo "$line" | sed -n 's/.*\[\([^]]*\)\](\(showcase\/[^)]*\)).*/\2/p' | head -1)
            
            if [ -n "$file_ref" ]; then
                # URL decode spaces and special characters
                file_ref=$(echo "$file_ref" | sed 's/%20/ /g')
                local full_path="$BASE_DIR/$file_ref"
                
                if [ ! -f "$full_path" ]; then
                    failed_files+=("$file_ref")
                fi
            fi
        fi
    done < "$readme_file"
    
    if [ ${#failed_files[@]} -eq 0 ]; then
        log_test_result "README showcase file references" 0
        return 0
    else
        local details="Missing files: ${failed_files[*]}"
        log_test_result "README showcase file references" 1 "$details"
        return 1
    fi
}

# Function: test_directory_references
# Description: Validates directory references like [_oldversions/](_oldversions/)  
# Parameters: None
# Returns: 0 if all directories exist, 1 if any missing
test_directory_references() {
    local readme_file="$BASE_DIR/README.md"
    local failed_dirs=()
    
    while IFS= read -r line; do
        if echo "$line" | grep -q '\[.*\](.*/)'; then
            # Extract directory path
            local dir_ref
            dir_ref=$(echo "$line" | sed -n 's/.*\[\([^]]*\)\](\([^)]*\/\)).*/\2/p' | head -1)
            
            if [ -n "$dir_ref" ]; then
                # Skip external URLs
                if [[ $dir_ref == http* || $dir_ref == ../* ]]; then
                    continue
                fi
                
                local full_path="$BASE_DIR/$dir_ref"
                if [ ! -d "$full_path" ]; then
                    failed_dirs+=("$dir_ref")
                fi
            fi
        fi
    done < "$readme_file"
    
    if [ ${#failed_dirs[@]} -eq 0 ]; then
        log_test_result "README directory references" 0
        return 0
    else
        local details="Missing directories: ${failed_dirs[*]}"
        log_test_result "README directory references" 1 "$details"
        return 1
    fi
}

# Function: test_no_empty_files
# Description: Validates that referenced files are not empty (size > 0)
# Parameters: None
# Returns: 0 if no empty files found, 1 if empty files exist
test_no_empty_files() {
    local empty_files=()
    
    # Check key framework files for content
    local key_files=(
        "2.5-refined-040125.md"
        "2.5-medium-071825.md" 
        "scratchpad-lite-071625.md"
        "README.md"
        "license.txt"
    )
    
    for file in "${key_files[@]}"; do
        local full_path="$BASE_DIR/$file"
        if [ -f "$full_path" ] && [ ! -s "$full_path" ]; then
            empty_files+=("$file")
        fi
    done
    
    if [ ${#empty_files[@]} -eq 0 ]; then
        log_test_result "No empty key files" 0
        return 0
    else
        local details="Empty files: ${empty_files[*]}"
        log_test_result "No empty key files" 1 "$details"
        return 1
    fi
}

# Function: test_markdown_syntax_basic
# Description: Basic markdown syntax validation for README.md
# Parameters: None
# Returns: 0 if syntax appears valid, 1 if issues found
test_markdown_syntax_basic() {
    local readme_file="$BASE_DIR/README.md"
    local issues=()
    
    # Check for unmatched markdown link brackets
    local unmatched_brackets
    unmatched_brackets=$(grep -n '\[.*\]([^)]*)' "$readme_file" | grep -v '\[.*\](.*)' || true)
    
    if [ -n "$unmatched_brackets" ]; then
        issues+=("Potential unmatched brackets")
    fi
    
    # Check for proper heading structure (should start with # not ##)
    local first_heading
    first_heading=$(grep -n '^#' "$readme_file" | head -1)
    
    if [[ $first_heading != *"# "* ]]; then
        issues+=("First heading should be level 1")
    fi
    
    if [ ${#issues[@]} -eq 0 ]; then
        log_test_result "Basic markdown syntax" 0
        return 0
    else
        local details="${issues[*]}"
        log_test_result "Basic markdown syntax" 1 "$details"
        return 1
    fi
}

# Function: print_summary
# Description: Prints comprehensive test results and statistics
# Parameters: None
# Returns: 0 if all tests passed, 1 if any failed
print_summary() {
    echo
    echo "=== Markdown Validation Summary ==="
    echo "Total Tests: $TEST_COUNT"
    echo "Passed:      $PASS_COUNT"  
    echo "Failed:      $FAIL_COUNT"
    echo
    
    if [ $FAIL_COUNT -eq 0 ]; then
        echo "All markdown validation tests PASSED! ✓"
        return 0
    else
        echo "Some markdown validation tests FAILED! ✗"
        echo "Please review the failed tests above and fix the issues."
        return 1
    fi
}

# Main test execution
main() {
    echo "=== Markdown Link Validation Test Suite ==="
    echo "Base directory: $BASE_DIR"
    echo
    
    cd "$BASE_DIR" || {
        echo "ERROR: Cannot change to base directory"
        exit 1
    }
    
    # Execute all test cases
    test_readme_framework_links
    test_readme_showcase_links  
    test_directory_references
    test_no_empty_files
    test_markdown_syntax_basic
    
    # Print results and exit
    print_summary
}

# Execute main function if script is run directly
if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
    main "$@"
fi