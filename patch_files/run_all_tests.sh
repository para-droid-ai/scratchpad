#!/bin/bash

#
# Master Test Runner for Scratchpad Repository
#
# DESCRIPTION:
#   A comprehensive test suite runner that executes all validation suites
#   for the Scratchpad framework repository. It is designed to be the single
#   point of entry for all repository validation, covering shell scripts,
#   markdown integrity, and framework template structure.
#
# USAGE:
#   ./run_all_tests.sh [--verbose] [--stop-on-failure]
#
# PARAMETERS:
#   --verbose           Show detailed output from each test suite.
#   --stop-on-failure   Exit immediately when any test suite fails.
#
# EXIT CODES:
#   0 - All test suites passed successfully.
#   1 - One or more test suites failed.
#

set -euo pipefail

# --- Configuration ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VERBOSE=false
STOP_ON_FAILURE=false
TOTAL_SUITES=0
PASSED_SUITES=0
FAILED_SUITES=0

# --- Functions ---

# Displays usage information and available options.
usage() {
    echo "Usage: $0 [OPTIONS]"
    echo
    echo "Master test runner for Scratchpad repository validation."
    echo
    echo "OPTIONS:"
    echo "  --verbose         Show detailed output from each test suite"
    echo "  --stop-on-failure Exit immediately when a test suite fails"
    echo "  --help            Display this help message"
}

# Parses command-line arguments and sets configuration flags.
parse_arguments() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --verbose) VERBOSITY=true; shift ;;
            --stop-on-failure) STOP_ON_FAILURE=true; shift ;;
            --help) usage; exit 0 ;;
            *) echo "ERROR: Unknown option '$1'" >&2; usage >&2; exit 1 ;;
        esac
    done
}

# Executes a single test suite, captures its result, and prints a summary.
# @param {string} suite_name - The human-readable name of the test suite.
# @param {string} script_path - The file path of the test script to execute.
# @returns {number} 0 if the test suite passed, 1 if it failed.
run_test_suite() {
    local suite_name="$1"
    local script_path="$2"
    
    TOTAL_SUITES=$((TOTAL_SUITES + 1))
    echo "=== Running $suite_name ==="
    
    if [ ! -f "$script_path" ] || [ ! -x "$script_path" ]; then
        echo "ERROR: Test script not found or not executable: $script_path" >&2
        FAILED_SUITES=$((FAILED_SUITES + 1))
        return 1
    fi
    
    local output
    local result
    
    if $VERBOSE; then
        # In verbose mode, show full, real-time output.
        bash "$script_path"
        result=$?
    else
        # In normal mode, capture output and show a summary.
        if output=$(bash "$script_path" 2>&1); then
            result=0
            echo "PASSED: $suite_name"
            echo "$output" | tail -n 2 # Show the last couple of lines for context
        else
            result=1
            echo "FAILED: $suite_name"
            echo "$output" | tail -n 5 # Show more lines on failure
        fi
    fi
    
    if [ $result -eq 0 ]; then
        PASSED_SUITES=$((PASSED_SUITES + 1))
        echo "✓ $suite_name completed successfully"
    else
        FAILED_SUITES=$((FAILED_SUITES + 1))
        echo "✗ $suite_name failed"
        if $STOP_ON_FAILURE; then
            echo "Stopping due to --stop-on-failure flag."
            exit 1
        fi
    fi
    
    echo
    return $result
}

# Ensures the environment has the necessary tools and structure to run the tests.
validate_test_environment() {
    local issues=()
    local required_commands=("bash" "grep" "find" "wc")
    
    for cmd in "${required_commands[@]}"; do
        if ! command -v "$cmd" >/dev/null 2>&1; then
            issues+=("Missing required command: $cmd")
        fi
    done
    
    if [ ! -d "$SCRIPT_DIR/../frameworks" ]; then
        issues+=("The 'frameworks' directory was not found.")
    fi
    
    if [ ${#issues[@]} -gt 0 ]; then
        echo "Environment validation failed:"
        printf "  - %s\n" "${issues[@]}"
        return 1
    fi
    
    return 0
}

# Prints the final summary of all test suite executions.
print_final_summary() {
    echo "================================================================"
    echo "                    FINAL TEST RESULTS"
    echo "================================================================"
    echo
    echo "Test Suites Executed: $TOTAL_SUITES"
    echo "Passed:              $PASSED_SUITES"
    echo "Failed:              $FAILED_SUITES"
    echo
    
    if [ $FAILED_SUITES -eq 0 ]; then
        echo "🎉 ALL TEST SUITES PASSED! 🎉"
        echo "Repository is ready for production use!"
    else
        echo "❌ $FAILED_SUITES TEST SUITE(S) FAILED ❌"
        echo "Please address the failing tests before proceeding."
    fi
}

# --- Main Execution ---
main() {
    parse_arguments "$@"
    
    echo "================================================================"
    echo "         SCRATCHPAD REPOSITORY TEST SUITE RUNNER"
    echo "================================================================"
    
    echo "=== Environment Validation ==="
    if ! validate_test_environment; then
        echo "Aborting due to environment issues."
        exit 1
    fi
    echo "✓ Environment validation passed"
    echo
    
    local test_suites=(
        "Remedial Script Tests:$SCRIPT_DIR/test_remedial_script.sh"
        "Markdown Link Validation:$SCRIPT_DIR/test_markdown_links.sh"
        "Framework Template Validation:$SCRIPT_DIR/test_framework_templates.sh"
        "Bug Fix Validation:$SCRIPT_DIR/test_bug_fixes.sh"
    )
    
    for suite_info in "${test_suites[@]}"; do
        run_test_suite "${suite_info%%:*}" "${suite_info##*:}"
    done
    
    print_final_summary
    
    if [ $FAILED_SUITES -gt 0 ]; then
        exit 1
    fi
}

main "$@"