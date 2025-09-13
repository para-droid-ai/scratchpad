#!/bin/bash

#
# Test Suite for Jules' Remedial Script
#
# DESCRIPTION:
#   Comprehensive test suite to validate the functionality and robustness
#   of the remedial.sh script. Tests include syntax validation, function
#   testing, error handling, and edge cases.
#
# USAGE:
#   ./test_remedial_script.sh
#
# REQUIREMENTS:
#   - Bash shell environment
#   - Access to jules-kit/scripts/remedial.sh
#
# EXIT CODES:
#   0 - All tests passed
#   1 - One or more tests failed
#

set -euo pipefail

# Test configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"
REMEDIAL_SCRIPT="$BASE_DIR/jules-kit/scripts/remedial.sh"
TEST_COUNT=0
PASS_COUNT=0
FAIL_COUNT=0

# Function: run_test
# Description: Executes a test case and tracks results
# Parameters:
#   $1 - Test name
#   $2 - Test command
# Returns: Updates global test counters
run_test() {
    local test_name="$1"
    local test_cmd="$2"
    
    TEST_COUNT=$((TEST_COUNT + 1))
    echo -n "Test $TEST_COUNT: $test_name ... "
    
    if eval "$test_cmd" >/dev/null 2>&1; then
        echo "PASS"
        PASS_COUNT=$((PASS_COUNT + 1))
        return 0
    else
        echo "FAIL"
        FAIL_COUNT=$((FAIL_COUNT + 1))
        return 1
    fi
}

# Function: test_script_exists
# Description: Validates that the remedial script file exists and is executable
# Parameters: None
# Returns: 0 if script exists and is executable, 1 otherwise
test_script_exists() {
    [ -f "$REMEDIAL_SCRIPT" ] && [ -x "$REMEDIAL_SCRIPT" ]
}

# Function: test_script_syntax
# Description: Validates bash syntax of the remedial script
# Parameters: None  
# Returns: 0 if syntax is valid, 1 otherwise
test_script_syntax() {
    bash -n "$REMEDIAL_SCRIPT"
}

# Function: test_script_execution
# Description: Tests that script executes without errors in a controlled environment
# Parameters: None
# Returns: 0 if script runs successfully, 1 otherwise
test_script_execution() {
    local temp_dir
    temp_dir=$(mktemp -d)
    
    # Create a safe environment for testing
    cd "$temp_dir" || return 1
    
    # Run the script with a timeout to prevent hanging
    timeout 30 bash "$REMEDIAL_SCRIPT" >/dev/null 2>&1
    local exit_code=$?
    
    # Clean up
    cd - >/dev/null || true
    rm -rf "$temp_dir"
    
    return $exit_code
}

# Function: test_error_log_creation  
# Description: Validates that script creates error.log file during execution
# Parameters: None
# Returns: 0 if error.log is created, 1 otherwise
test_error_log_creation() {
    local temp_dir
    temp_dir=$(mktemp -d)
    
    cd "$temp_dir" || return 1
    timeout 30 bash "$REMEDIAL_SCRIPT" >/dev/null 2>&1 || true
    
    local result=1
    if [ -f "error.log" ]; then
        result=0
    fi
    
    cd - >/dev/null || true
    rm -rf "$temp_dir"
    
    return $result
}

# Function: test_docker_detection
# Description: Tests that script properly detects absence of docker-compose files
# Parameters: None  
# Returns: 0 if detection works correctly, 1 otherwise
test_docker_detection() {
    local temp_dir
    temp_dir=$(mktemp -d)
    
    cd "$temp_dir" || return 1
    local output
    output=$(timeout 30 bash "$REMEDIAL_SCRIPT" 2>&1)
    
    cd - >/dev/null || true
    rm -rf "$temp_dir"
    
    # Should contain message about no docker compose file
    echo "$output" | grep -q "No Docker Compose file found"
}

# Function: print_summary
# Description: Prints test execution summary with pass/fail statistics  
# Parameters: None
# Returns: None
print_summary() {
    echo
    echo "=== Test Summary ==="
    echo "Total Tests: $TEST_COUNT"
    echo "Passed:      $PASS_COUNT"
    echo "Failed:      $FAIL_COUNT"
    echo
    
    if [ $FAIL_COUNT -eq 0 ]; then
        echo "All tests PASSED! ✓"
        return 0
    else
        echo "Some tests FAILED! ✗"
        return 1
    fi
}

# Main test execution
main() {
    echo "=== Remedial Script Test Suite ==="
    echo "Testing script: $REMEDIAL_SCRIPT"
    echo
    
    # Execute test cases
    run_test "Script file exists and is executable" "test_script_exists"
    run_test "Script has valid bash syntax" "test_script_syntax"  
    run_test "Script executes without errors" "test_script_execution"
    run_test "Script creates error.log file" "test_error_log_creation"
    run_test "Script properly detects Docker setup" "test_docker_detection"
    
    # Print results and exit with appropriate code
    print_summary
}

# Execute main function if script is run directly
if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
    main "$@"
fi