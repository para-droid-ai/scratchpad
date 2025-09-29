#!/bin/bash

#
# Bug Fix Validation Test Suite
#
# DESCRIPTION:
#   This test suite serves as a regression tool to verify that specific,
#   known bugs in the repository have been successfully fixed and remain fixed.
#   It checks for issues ranging from broken file links to incorrect script logic.
#
# USAGE:
#   ./test_bug_fixes.sh
#
# BUGS TESTED:
#   - Major Bug: Broken asset file references in the main README.md.
#   - Minor Bug: A script referencing a non-existent `remedial_v2.sh`.
#   - Minor Bug: A script using a hardcoded, non-portable `/app` directory path.
#   - Minor Bug: An empty, corrupted GIF file in the repository root.
#   - Minor Bug: A filename typo ("protocal" instead of "protocol").
#
# EXIT CODES:
#   0 - All bug fix validation tests passed.
#   1 - One or more bugs are still present or have regressed.
#

set -euo pipefail

# --- Test Configuration ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"
TEST_COUNT=0
PASS_COUNT=0
FAIL_COUNT=0

# --- Functions ---

# Logs and tracks the result of a single bug fix test.
log_test_result() {
    local test_name="$1"
    local result="$2"
    local details="${3:-}"
    
    TEST_COUNT=$((TEST_COUNT + 1))
    printf "Bug Fix Test %d: %s ... " "$TEST_COUNT" "$test_name"
    
    if [ "$result" -eq 0 ]; then
        printf "FIXED ✓\n"
        PASS_COUNT=$((PASS_COUNT + 1))
    else
        printf "BROKEN ✗\n"
        [ -n "$details" ] && printf "  Details: %s\n" "$details"
        FAIL_COUNT=$((FAIL_COUNT + 1))
    fi
}

# Validates that asset file references in the README are now correct.
test_asset_file_references_fixed() {
    local missing_files=()
    local asset_files=(
        "assets/4%20images.png"
        "assets/scratchpad%20from%20main_new.gif"
        "assets/create%20scratchpad%20collection.gif"
        "assets/TLDR%20Task%20with%20Canvas.png"
    )
    
    for file in "${asset_files[@]}"; do
        local decoded_file
        decoded_file=$(printf '%b' "${file//%/\\x}")
        if [ ! -f "$BASE_DIR/$decoded_file" ]; then
            missing_files+=("$decoded_file")
        fi
    done
    
    if [ ${#missing_files[@]} -eq 0 ]; then
        log_test_result "Major Bug - Asset file references" 0
    else
        log_test_result "Major Bug - Asset file references" 1 "Missing: ${missing_files[*]}"
    fi
}

# Validates that remedial.sh no longer references a non-existent v2 script.
test_remedial_script_no_longer_references_v2() {
    local remedial_script="$BASE_DIR/scripts/remedial.sh"
    if grep -q "remedial_v2.sh" "$remedial_script"; then
        log_test_result "Minor Bug 1 - remedial_v2.sh reference" 1 "Still references remedial_v2.sh"
    else
        log_test_result "Minor Bug 1 - remedial_v2.sh reference removed" 0
    fi
}

# Validates that remedial.sh correctly changes to the base directory before executing.
test_remedial_script_runs_from_base_dir() {
    local remedial_script="$BASE_DIR/scripts/remedial.sh"
    local output
    output=$(bash "$remedial_script" 2>&1)

    if echo "$output" | grep -q "Current directory: $BASE_DIR"; then
        log_test_result "Minor Bug 2 - Runs from base dir" 0
    else
        log_test_result "Minor Bug 2 - Runs from base dir" 1 "Script did not run from the expected base directory."
    fi
}

# Validates that the corrupted empty GIF file was removed.
test_empty_gif_file_removed() {
    local empty_gif="$BASE_DIR/assets/scratchpad-from-main_new.gif"
    if [ -f "$empty_gif" ] && [ ! -s "$empty_gif" ]; then
        log_test_result "Minor Bug 3 - empty gif file" 1 "Empty gif file still present"
    else
        log_test_result "Minor Bug 3 - empty gif file removed" 0
    fi
}

# Validates that the "protocal" filename typo was fixed to "protocol".
test_filename_typo_fixed() {
    if [ -f "$BASE_DIR/assets/thinking_scratchpad_protocal.gif" ]; then
        log_test_result "Minor Bug 4 - filename typo 'protocal'" 1 "Typo file still exists"
    elif [ ! -f "$BASE_DIR/assets/thinking_scratchpad_protocol.gif" ]; then
        log_test_result "Minor Bug 4 - filename typo 'protocal'" 1 "Corrected file not found"
    else
        log_test_result "Minor Bug 4 - filename typo fixed to 'protocol'" 0
    fi
}

# Validates that the fixed remedial script executes without errors.
test_remedial_script_functionality() {
    if timeout 30 bash "$BASE_DIR/scripts/remedial.sh" >/dev/null 2>&1; then
        log_test_result "Remedial script functionality after fixes" 0
    else
        log_test_result "Remedial script functionality after fixes" 1 "Script fails to execute"
    fi
}

# Prints the final summary of the bug fix validation tests.
print_bug_fix_summary() {
    printf "\n=== Bug Fix Validation Summary ===\n"
    printf "Total Bug Tests: %d\n" "$TEST_COUNT"
    printf "Bugs Fixed:      %d\n" "$PASS_COUNT"
    printf "Still Broken:    %d\n\n" "$FAIL_COUNT"
    if [ $FAIL_COUNT -eq 0 ]; then
        printf "🐛➜✅ ALL IDENTIFIED BUGS HAVE BEEN FIXED! 🐛➜✅\n"
    else
        printf "⚠️  %d BUG(S) STILL PRESENT OR FIXES BROKEN ⚠️\n" "$FAIL_COUNT"
    fi
}

# --- Main Execution ---
main() {
    printf "=== Bug Fix Validation Test Suite ===\n"
    cd "$BASE_DIR" || exit 1
    
    test_asset_file_references_fixed
    test_remedial_script_no_longer_references_v2
    test_remedial_script_runs_from_base_dir
    test_empty_gif_file_removed
    test_filename_typo_fixed
    test_remedial_script_functionality
    
    print_bug_fix_summary
    
    if [ $FAIL_COUNT -gt 0 ]; then
        exit 1
    fi
}

main "$@"