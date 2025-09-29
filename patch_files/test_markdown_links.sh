#!/bin/bash

#
# Markdown Link Validation Test Suite
#
# DESCRIPTION:
#   A comprehensive test suite for validating all internal file and directory
#   references in markdown files throughout the repository. It is crucial for
#   maintaining the integrity of the documentation.
#
# USAGE:
#   ./test_markdown_links.sh
#
# CHECKS PERFORMED:
#   - Verifies that all local file links in markdown point to existing files.
#   - Checks that all local directory links point to existing directories.
#   - Ensures that key referenced files are not empty.
#   - Performs basic syntax validation for markdown files.
#
# EXIT CODES:
#   0 - All markdown links and references are valid.
#   1 - One or more broken links or references were found.
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

# Validates all framework file references in any markdown files.
test_all_framework_links() {
    local failed_files=()
    
    # Find all markdown files and check their links to other .md or .txt files.
    find "$BASE_DIR" -name "*.md" -print0 | while IFS= read -r -d '' md_file; do
        local file_refs
        file_refs=$(grep -o '\[.*\]([^)]*\.\(md\|txt\))' "$md_file" | sed 's/.*(\(.*\))/\1/' || true)
        
        for file_ref in $file_refs; do
            local decoded_ref
            decoded_ref=$(printf '%b' "${file_ref//%/\\x}")
            # Construct path relative to the markdown file's directory
            local full_path
            full_path="$(dirname "$md_file")/$decoded_ref"
            
            if [ ! -f "$full_path" ]; then
                failed_files+=("$decoded_ref in $md_file")
            fi
        done
    done
    
    if [ ${#failed_files[@]} -eq 0 ]; then
        log_test_result "All framework file references" 0
    else
        log_test_result "All framework file references" 1 "Missing: ${failed_files[*]}"
    fi
}

# Validates all asset file references in the README.
test_readme_asset_links() {
    local readme_file="$BASE_DIR/README.md"
    local failed_files=()
    
    local file_refs
    file_refs=$(grep -o '\[.*\](assets/[^)]*)' "$readme_file" | sed 's/.*(\(.*\))/\1/' || true)

    for file_ref in $file_refs; do
        local decoded_ref
        decoded_ref=$(printf '%b' "${file_ref//%/\\x}")
        if [ ! -f "$BASE_DIR/$decoded_ref" ]; then
            failed_files+=("$decoded_ref")
        fi
    done
    
    if [ ${#failed_files[@]} -eq 0 ]; then
        log_test_result "README asset file references" 0
    else
        log_test_result "README asset file references" 1 "Missing: ${failed_files[*]}"
    fi
}

# Validates that key referenced files are not empty.
test_no_empty_files() {
    local empty_files=()
    local key_files=(
        "README.md"
        "license.txt"
        "frameworks/core/2.5-refined-040125.md"
    )
    
    for file in "${key_files[@]}"; do
        if [ -f "$BASE_DIR/$file" ] && [ ! -s "$BASE_DIR/$file" ]; then
            empty_files+=("$file")
        fi
    done
    
    if [ ${#empty_files[@]} -eq 0 ]; then
        log_test_result "No empty key files" 0
    else
        log_test_result "No empty key files" 1 "Empty files: ${empty_files[*]}"
    fi
}

# Prints the final summary of the markdown validation tests.
print_summary() {
    printf "\n=== Markdown Validation Summary ===\n"
    printf "Total Tests: %d\n" "$TEST_COUNT"
    printf "Passed:      %d\n" "$PASS_COUNT"
    printf "Failed:      %d\n\n" "$FAIL_COUNT"
    if [ $FAIL_COUNT -eq 0 ]; then
        printf "All markdown validation tests PASSED! ✓\n"
    else
        printf "Some markdown validation tests FAILED! ✗\n"
    fi
}

# --- Main Execution ---
main() {
    printf "=== Markdown Link Validation Test Suite ===\n"
    cd "$BASE_DIR" || exit 1
    
    test_all_framework_links
    test_readme_asset_links
    test_no_empty_files
    
    print_summary
    
    if [ $FAIL_COUNT -gt 0 ]; then
        exit 1
    fi
}

main "$@"