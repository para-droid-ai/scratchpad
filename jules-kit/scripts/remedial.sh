#!/bin/bash

#
# Jules' Remedial Recovery Script
#
# DESCRIPTION:
#   A comprehensive recovery and diagnostic script for development environments.
#   Provides automated recovery procedures for common development issues including
#   Docker access, permission problems, and environment setup.
#
# USAGE:
#   ./remedial.sh
#
# REQUIREMENTS:
#   - Bash shell environment
#   - Docker (optional, for container-related recovery)
#   - sudo access for system-level repairs
#
# OUTPUT:
#   - Environment diagnostic information
#   - Error logs captured to error.log file
#   - Recovery status messages
#
# EXIT CODES:
#   0 - Success
#   1 - General error
#   2 - Missing required dependencies
#
# AUTHOR: Jules' Remedial Framework
# VERSION: 1.0
#

# Set strict error handling
set -euo pipefail

# Function: main_recovery_procedure
# Description: Executes the main recovery workflow including environment checks
#              and Docker permission fixes for Linux environments
# Parameters: None
# Returns: Exit code 0 on success, non-zero on failure
main_recovery_procedure() {
    local script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    local base_dir="$(dirname "$(dirname "$script_dir")")"
    
    echo "=== Jules' Remedial Recovery Starting ==="
    echo "Script directory: $script_dir"
    echo "Base directory: $base_dir"
    
    # Change to base directory instead of hardcoded /app
    cd "$base_dir" || {
        echo "ERROR: Cannot change to base directory: $base_dir" >&2
        return 1
    }
    
    # Sanity check - display current directory contents
    echo "=== Current Directory Contents ==="
    ls -la
    
    # Docker access recovery for Linux environments
    if [[ "$OSTYPE" == "linux-gnu"* ]] && command -v docker >/dev/null 2>&1; then
        echo "=== Docker Permission Recovery ==="
        
        # Check if docker-compose exists, skip docker setup if not needed
        if [ -f "docker-compose.yml" ] || [ -f "docker-compose.yaml" ]; then
            echo "Docker Compose file found, ensuring daemon access..."
            
            # Fix docker socket permissions (requires re-login for group to apply)
            if ! groups | grep -q docker; then
                echo "Adding user to docker group..."
                sudo usermod -aG docker "$USER" && newgrp docker
            else
                echo "User already in docker group"
            fi
        else
            echo "No Docker Compose file found, skipping Docker setup"
        fi
    else
        echo "Skipping Docker setup (not Linux or Docker not installed)"
    fi
    
    echo "=== Recovery Complete ==="
    return 0
}

# Execute main procedure and capture all output
main_recovery_procedure 2>&1 | tee error.log