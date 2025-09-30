#!/bin/bash

#
# Framework Template Validation Test Suite
#
# DESCRIPTION:
#   Validates the integrity and completeness of all Scratchpad framework
#   templates in the repository. It checks for file existence, content,
#   and structural consistency to ensure all frameworks are usable.
#
# USAGE:
#   ./test_framework_templates.sh
#
# CHECKS PERFORMED:
#   - Existence of all core and purpose-built framework files.
#   - Ensures that framework files are not empty or trivially small.
#   - Validates the internal structure of purpose-built frameworks for key headers.
#
# EXIT CODES:
#   0 - All template validation tests passed.
#   1 - One or more template validation tests failed.
#

set -euo pipefail

# --- Test Configuration ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"
TEST_COUNT=0
PASS_COUNT=0
FAIL_COUNT=0

# --- Functions ---

# Logs and tracks the result of a single test case.
log_test_result() {
    local test_name="$1"
    local result="$2"
    local details="${3:-}"
    
    TEST_COUNT=$((TEST_COUNT + 1))
    printf "Test %d: %s ... " "$TEST_COUNT" "$test_name"
    
    if [ "$result" -eq 0 ]; then
        printf "PASS\n"
        PASS_COUNT=$((PASS_COUNT + 1))
    else
        printf "FAIL\n"
        [ -n "$details" ] && printf "  Details: %s\n" "$details"
        FAIL_COUNT=$((FAIL_COUNT + 1))
    fi
}

# Validates that all core framework files exist in their new location.
test_core_frameworks_exist() {
    local missing_files=()
    local core_files=(
        "frameworks/core/2.5-refined-040125.md"
        "frameworks/core/2.5-medium-071825.md"
        "frameworks/core/scratchpad-lite-071625.md"
    )
    
    for file in "${core_files[@]}"; do
        if [ ! -f "$BASE_DIR/$file" ]; then
            missing_files+=("$file")
        fi
    done
    
    if [ ${#missing_files[@]} -eq 0 ]; then
        log_test_result "Core framework files exist" 0
    else
        log_test_result "Core framework files exist" 1 "Missing: ${missing_files[*]}"
    fi
}

# Validates that framework files have meaningful content (>100 bytes).
test_frameworks_not_empty() {
    local small_files=()
    local min_size=100
    
    # Use find with process substitution to handle filenames with spaces correctly.
    # Target the new frameworks directory and exclude legacy files.
    while IFS= read -r file; do
        if [ -s "$file" ] && [ "$(wc -c <"$file")" -lt $min_size ]; then
            small_files+=("$(basename "$file")")
        fi
    done < <(find "$BASE_DIR/frameworks" -type f \( -name "*.md" -o -name "*.txt" \) -not -path "*/legacy/*")
    
    if [ ${#small_files[@]} -eq 0 ]; then
        log_test_result "Frameworks have adequate content" 0
    else
        log_test_result "Frameworks have adequate content" 1 "Small files: ${small_files[*]}"
    fi
}

# Validates the internal structure of purpose-built framework files.
test_purpose_built_framework_structure() {
    local malformed_files=()
    
    # Use find with process substitution to target the new purpose-built directory.
    while IFS= read -r file; do
        if [[ "$file" == *.md ]]; then
            local header_count
            header_count=$(grep -c "^## " "$file" || true)
            if [ "$header_count" -lt 3 ]; then
                malformed_files+=("$(basename "$file") (has only $header_count L2 headers)")
            fi
        elif [[ "$file" == *.txt ]]; then
            local separator_count
            separator_count=$(grep -c -E "(^----+$|^====+$)" "$file" || true)
             if [ "$separator_count" -lt 3 ]; then
                malformed_files+=("$(basename "$file") (has only $separator_count separators)")
            fi
        fi
    done < <(find "$BASE_DIR/frameworks/purpose-built" -type f \( -name "*.md" -o -name "*.txt" \))

    if [ ${#malformed_files[@]} -eq 0 ]; then
        log_test_result "Purpose-built frameworks have a valid structure" 0
    else
        log_test_result "Purpose-built frameworks have a valid structure" 1 "Malformed: ${malformed_files[*]}"
    fi
}

# Prints the final summary of the framework template validation tests.
print_summary() {
    printf "\n=== Framework Template Validation Summary ===\n"
    printf "Total Tests: %d\n" "$TEST_COUNT"
    printf "Passed:      %d\n" "$PASS_COUNT"
    printf "Failed:      %d\n\n" "$FAIL_COUNT"
    if [ $FAIL_COUNT -eq 0 ]; then
        printf "All framework validation tests PASSED! ✓\n"
    else
        printf "Some framework validation tests FAILED! ✗\n"
    fi
}

# --- Main Execution ---
main() {
    printf "=== Framework Template Validation Test Suite ===\n"
    cd "$BASE_DIR" || exit 1
    
    test_core_frameworks_exist
    test_frameworks_not_empty
    test_purpose_built_framework_structure
    
    print_summary
    
    if [ $FAIL_COUNT -gt 0 ]; then
        exit 1
    fi
}

main "$@"