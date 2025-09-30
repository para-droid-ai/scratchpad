#!/bin/bash

#
# Test Suite for Jules' Remedial Script
#
# DESCRIPTION:
#   A comprehensive test suite to validate the functionality, robustness, and
#   correctness of the `remedial.sh` script. It covers basic execution,
#   error handling, and specific logic paths like Docker permission checks.
#
# USAGE:
#   ./test_remedial_script.sh
#
# CHECKS PERFORMED:
#   - Script existence, executability, and bash syntax.
#   - Correct creation of the `error.log` file in the repository root.
#   - Proper detection of the repository's base directory.
#   - Graceful handling of scenarios where Docker is not in use.
#   - Correct logic for suggesting `usermod` for Docker permissions.
#
# EXIT CODES:
#   0 - All tests passed.
#   1 - One or more tests failed.
#

set -euo pipefail

# --- Test Configuration ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"
REMEDIAL_SCRIPT="$BASE_DIR/scripts/remedial.sh"
TEST_COUNT=0
PASS_COUNT=0
FAIL_COUNT=0

# --- Test Runner ---

# Executes a single test case and tracks the result.
# @param {string} test_name - The human-readable name of the test.
# @param {string} test_cmd - The command to execute for the test.
run_test() {
    local test_name="$1"
    local test_cmd="$2"
    
    TEST_COUNT=$((TEST_COUNT + 1))
    echo -n "Test $TEST_COUNT: $test_name ... "
    
    if eval "$test_cmd"; then
        echo "PASS"
        PASS_COUNT=$((PASS_COUNT + 1))
    else
        echo "FAIL"
        FAIL_COUNT=$((FAIL_COUNT + 1))
    fi
}

# --- Test Cases ---

# Validates that the script file exists and is executable.
test_script_exists() {
    [ -f "$REMEDIAL_SCRIPT" ] && [ -x "$REMEDIAL_SCRIPT" ]
}

# Validates the bash syntax of the remedial script.
test_script_syntax() {
    bash -n "$REMEDIAL_SCRIPT" >/dev/null 2>&1
}

# Tests that the script executes without fatal errors.
test_script_execution() {
    timeout 30 bash "$REMEDIAL_SCRIPT" >/dev/null 2>&1
}

# Validates that the script creates the error.log file in the project root.
test_error_log_creation_in_root() {
    rm -f "$BASE_DIR/error.log"
    (cd /tmp && timeout 30 bash "$REMEDIAL_SCRIPT" >/dev/null 2>&1 || true)
    
    if [ -f "$BASE_DIR/error.log" ]; then
        rm -f "$BASE_DIR/error.log"
        return 0
    else
        return 1
    fi
}

# Verifies that the script correctly operates from the base directory.
test_base_dir_detection() {
    local output
    output=$(bash "$REMEDIAL_SCRIPT" 2>&1)
    echo "$output" | grep -q "Current directory: $BASE_DIR"
}

# Mocks the environment to test the Docker permission check logic.
test_docker_permission_logic() {
    local temp_dir
    temp_dir=$(mktemp -d)
    
    # Create mock 'groups' and 'sudo' commands
    echo '#!/bin/bash' > "$temp_dir/groups" && echo 'echo "not_a_docker_user"' >> "$temp_dir/groups"
    echo '#!/bin/bash' > "$temp_dir/sudo" && echo 'echo "usermod_called_with: $*"' >> "$temp_dir/sudo"
    chmod +x "$temp_dir/groups" "$temp_dir/sudo"
    
    touch "$BASE_DIR/docker-compose.yml"
    
    local output
    output=$(PATH=$temp_dir:$PATH timeout 30 bash "$REMEDIAL_SCRIPT" 2>&1)
    
    rm -f "$BASE_DIR/docker-compose.yml"
    rm -rf "$temp_dir"
    
    echo "$output" | grep -q "User not in 'docker' group" && \
    echo "$output" | grep -q "usermod_called_with: usermod -aG docker $USER"
}

# Ensures the script gracefully skips Docker checks when no docker-compose file is present.
test_no_docker_compose_scenario() {
    rm -f "$BASE_DIR/docker-compose.yml"
    local output
    output=$(timeout 30 bash "$REMEDIAL_SCRIPT" 2>&1)
    echo "$output" | grep -q "No Docker Compose file found, skipping Docker setup"
}

# Verifies that the log file contains expected output.
test_log_file_content() {
    rm -f "$BASE_DIR/error.log"
    timeout 30 bash "$REMEDIAL_SCRIPT" >/dev/null 2>&1 || true
    
    if [ ! -f "$BASE_DIR/error.log" ]; then return 1; fi
    
    if grep -q "=== Jules' Remedial Recovery Starting ===" "$BASE_DIR/error.log"; then
        rm -f "$BASE_DIR/error.log"
        return 0
    else
        rm -f "$BASE_DIR/error.log"
        return 1
    fi
}

# --- Test Runner Main ---

# Prints the final summary of the test execution.
print_summary() {
    echo
    echo "=== Test Summary ==="
    echo "Total Tests: $TEST_COUNT"
    echo "Passed:      $PASS_COUNT"
    echo "Failed:      $FAIL_COUNT"
    echo
    
    if [ $FAIL_COUNT -eq 0 ]; then
        echo "All tests PASSED! ✓"
        exit 0
    else
        echo "Some tests FAILED! ✗"
        exit 1
    fi
}

# Main function to run all test cases.
main() {
    echo "=== Remedial Script Test Suite (Enhanced) ==="
    
    run_test "Script file exists and is executable" "test_script_exists"
    run_test "Script has valid bash syntax" "test_script_syntax"
    run_test "Script executes without errors" "test_script_execution"
    run_test "Script creates error.log in root" "test_error_log_creation_in_root"
    run_test "Log file contains expected output" "test_log_file_content"
    run_test "Script correctly runs from base directory" "test_base_dir_detection"
    run_test "Script skips Docker check without compose file" "test_no_docker_compose_scenario"
    run_test "Script suggests 'usermod' for Docker permissions" "test_docker_permission_logic"
    
    print_summary
}

main "$@"