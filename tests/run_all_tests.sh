#!/bin/bash

#
# Master Test Runner for Scratchpad Repository
#
# DESCRIPTION:
#   Comprehensive test suite runner that executes all validation tests
#   for the Scratchpad framework repository. Includes shell script testing,
#   markdown validation, and framework template validation.
#
# USAGE:
#   ./run_all_tests.sh [--verbose] [--stop-on-failure]
#
# PARAMETERS:
#   --verbose        Show detailed output from each test suite
#   --stop-on-failure Exit immediately when a test suite fails
#
# EXIT CODES:
#   0 - All test suites passed
#   1 - One or more test suites failed
#

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VERBOSE=false
STOP_ON_FAILURE=false
TOTAL_SUITES=0
PASSED_SUITES=0
FAILED_SUITES=0

# Function: usage
# Description: Display usage information and available options
# Parameters: None
# Returns: None
usage() {
    echo "Usage: $0 [OPTIONS]"
    echo
    echo "Master test runner for Scratchpad repository validation."
    echo
    echo "OPTIONS:"
    echo "  --verbose         Show detailed output from each test suite"
    echo "  --stop-on-failure Exit immediately when a test suite fails"
    echo "  --help           Display this help message"
    echo
    echo "EXAMPLES:"
    echo "  $0                    # Run all tests with summary output"
    echo "  $0 --verbose          # Run all tests with detailed output"
    echo "  $0 --stop-on-failure  # Stop at first test suite failure"
}

# Function: parse_arguments
# Description: Parse command line arguments and set configuration flags
# Parameters: All command line arguments
# Returns: None (sets global variables)
parse_arguments() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --verbose)
                VERBOSE=true
                shift
                ;;
            --stop-on-failure)
                STOP_ON_FAILURE=true
                shift
                ;;
            --help)
                usage
                exit 0
                ;;
            *)
                echo "ERROR: Unknown option '$1'" >&2
                usage >&2
                exit 1
                ;;
        esac
    done
}

# Function: run_test_suite
# Description: Execute a test suite and capture results
# Parameters:
#   $1 - Test suite name
#   $2 - Test script path
# Returns: 0 if test suite passed, 1 if failed
run_test_suite() {
    local suite_name="$1"
    local script_path="$2"
    
    TOTAL_SUITES=$((TOTAL_SUITES + 1))
    
    echo "=== Running $suite_name ==="
    
    if [ ! -f "$script_path" ]; then
        echo "ERROR: Test script not found: $script_path" >&2
        FAILED_SUITES=$((FAILED_SUITES + 1))
        return 1
    fi
    
    if [ ! -x "$script_path" ]; then
        echo "ERROR: Test script not executable: $script_path" >&2
        FAILED_SUITES=$((FAILED_SUITES + 1))
        return 1
    fi
    
    local output result
    
    if $VERBOSE; then
        # Show full output in verbose mode
        if bash "$script_path"; then
            result=0
        else
            result=1
        fi
    else
        # Capture output and show summary
        if output=$(bash "$script_path" 2>&1); then
            result=0
            echo "PASSED: $suite_name"
            # Show just the summary line
            echo "$output" | tail -1
        else
            result=1
            echo "FAILED: $suite_name"
            echo "$output" | tail -5  # Show last few lines including error
        fi
    fi
    
    if [ $result -eq 0 ]; then
        PASSED_SUITES=$((PASSED_SUITES + 1))
        echo "✓ $suite_name completed successfully"
    else
        FAILED_SUITES=$((FAILED_SUITES + 1))
        echo "✗ $suite_name failed"
        
        if $STOP_ON_FAILURE; then
            echo "Stopping due to --stop-on-failure flag"
            return 1
        fi
    fi
    
    echo
    return $result
}

# Function: validate_test_environment
# Description: Ensure the test environment is properly set up
# Parameters: None
# Returns: 0 if environment valid, 1 if issues found
validate_test_environment() {
    local issues=()
    
    # Check for required commands
    local required_commands=("bash" "grep" "sed" "find" "wc")
    
    for cmd in "${required_commands[@]}"; do
        if ! command -v "$cmd" >/dev/null 2>&1; then
            issues+=("Missing command: $cmd")
        fi
    done
    
    # Check that we're in the right directory structure
    if [ ! -f "$SCRIPT_DIR/../README.md" ]; then
        issues+=("README.md not found in expected location")
    fi
    
    if [ ! -d "$SCRIPT_DIR/../purpose-built" ]; then
        issues+=("purpose-built directory not found")
    fi
    
    if [ ${#issues[@]} -gt 0 ]; then
        echo "Environment validation failed:"
        printf "  - %s\n" "${issues[@]}"
        return 1
    fi
    
    return 0
}

# Function: print_final_summary
# Description: Print comprehensive results summary
# Parameters: None
# Returns: 0 if all suites passed, 1 if any failed
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
        echo
        echo "The Scratchpad repository has been thoroughly validated:"
        echo "  ✓ Shell scripts are functional and well-documented"
        echo "  ✓ Markdown links and references are valid"  
        echo "  ✓ Framework templates are complete and accessible"
        echo "  ✓ All identified bugs have been fixed and verified"
        echo
        echo "Repository is ready for production use!"
        return 0
    else
        echo "❌ $FAILED_SUITES TEST SUITE(S) FAILED ❌"
        echo
        echo "Please address the failing tests before proceeding."
        echo "Use --verbose flag for detailed error information."
        return 1
    fi
}

# Main execution function
main() {
    parse_arguments "$@"
    
    echo "================================================================"
    echo "         SCRATCHPAD REPOSITORY TEST SUITE RUNNER"
    echo "================================================================"
    echo "Verbose mode: $VERBOSE"
    echo "Stop on failure: $STOP_ON_FAILURE"
    echo
    
    # Validate environment first
    echo "=== Environment Validation ==="
    if ! validate_test_environment; then
        echo "Environment validation failed. Cannot continue."
        exit 1
    fi
    echo "✓ Environment validation passed"
    echo
    
    # Define test suites to run
    local test_suites=(
        "Remedial Script Tests:$SCRIPT_DIR/test_remedial_script.sh"
        "Markdown Link Validation:$SCRIPT_DIR/test_markdown_links.sh"
        "Framework Template Validation:$SCRIPT_DIR/test_framework_templates.sh"
        "Bug Fix Validation:$SCRIPT_DIR/test_bug_fixes.sh"
    )
    
    # Execute each test suite
    local overall_result=0
    
    for suite_info in "${test_suites[@]}"; do
        local suite_name="${suite_info%%:*}"
        local script_path="${suite_info##*:}"
        
        if ! run_test_suite "$suite_name" "$script_path"; then
            overall_result=1
            if $STOP_ON_FAILURE; then
                break
            fi
        fi
    done
    
    # Print final summary
    print_final_summary
    exit $overall_result
}

# Execute main function if script is run directly
if [ "${BASH_SOURCE[0]}" == "${0}" ]; then
    main "$@"
fi