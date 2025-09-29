#!/bin/bash

#
# Jules' Remedial Recovery Script
#
# DESCRIPTION:
#   A comprehensive recovery and diagnostic script for development environments.
#   It provides automated recovery procedures for common issues, including Docker
#   permissions, and ensures a consistent operational environment. The script is
#   designed to be idempotent and safe to run multiple times.
#
# USAGE:
#   ./jules-kit/scripts/remedial.sh
#
# REQUIREMENTS:
#   - Bash shell environment (v4.0+ recommended)
#   - Docker (optional, for container-related recovery)
#   - sudo access for system-level repairs (e.g., 'usermod')
#
# OUTPUT:
#   - Environment diagnostic information (e.g., directory paths)
#   - Status messages for each recovery step.
#   - All output is captured to 'error.log' in the repository root.
#
# EXIT CODES:
#   0 - Success: The script completed all tasks without fatal errors.
#   1 - General error: A critical operation failed (e.g., changing directory).
#
# AUTHOR: Jules' Remedial Framework
# VERSION: 1.5
#

# --- Strict Mode ---
set -euo pipefail

# --- Main Recovery Procedure ---
#
# Executes the main recovery workflow. This function assumes it is being run
# from the repository's base directory.
#
# Parameters:
#   None
#
# Returns:
#   - 0 on successful completion.
#
main_recovery_procedure() {
    printf "=== Jules' Remedial Recovery Starting ===\n"
    printf "Current directory: %s\n" "$(pwd)"
    
    # Perform a sanity check by listing the contents of the current directory.
    printf "=== Current Directory Contents ===\n"
    ls -la || true # Bug fix: prevent exit on error
    
    # --- Docker Permission Recovery for Linux ---
    if [[ "$OSTYPE" == "linux-gnu"* ]] && command -v docker >/dev/null 2>&1; then
        printf "=== Docker Permission Recovery ===\n"
        if [ -f "docker-compose.yml" ] || [ -f "docker-compose.yaml" ]; then
            printf "Docker Compose file found, ensuring daemon access...\n"
            if ! groups | grep -q '\bdocker\b'; then
                printf "User not in 'docker' group. Adding...\n"
                # Bug fix: Removed ineffective 'newgrp docker'
                sudo usermod -aG docker "$USER"
                printf "INFO: User '%s' added to the 'docker' group. Please log out and log back in for this to take effect.\n" "$USER"
            else
                printf "User already in 'docker' group.\n"
            fi
        else
            printf "No Docker Compose file found, skipping Docker setup.\n"
        fi
    else
        printf "Skipping Docker setup (not Linux or Docker not installed).\n"
    fi
    
    printf "=== Recovery Complete ===\n"
    return 0
}

# --- Script Execution ---
# Determine the repository's base directory to ensure paths are resolved correctly.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"

# Change to the base directory first to ensure all subsequent commands,
# including the log redirection, execute from the correct location.
cd "$BASE_DIR" || {
    printf "FATAL: Could not change to base directory '%s'. Aborting.\n" "$BASE_DIR" >&2
    exit 1
}

# Execute the main procedure and capture all output to the 'error.log' file
# in the current directory (which is now the repository root).
main_recovery_procedure 2>&1 | tee "error.log"