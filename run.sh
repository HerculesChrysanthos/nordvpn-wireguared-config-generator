#!/bin/bash

set -e

# Check for Python 3
if command -v python3 &>/dev/null; then
    PYTHON_CMD="python3"
elif command -v python &>/dev/null; then
    version=$(python -c 'import sys; print(sys.version_info[0])')
    if [ "$version" -eq 3 ]; then
        PYTHON_CMD="python"
    else
        echo "ERROR: Python 3 is required but found Python 2"
        exit 1
    fi
else
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3 to continue. You can download it from:"
    echo "https://www.python.org/downloads/"
    exit 1
fi

echo "Found Python 3 installation: $($PYTHON_CMD --version)"

# Clear screen
clear

# Prompt for NordVPN API token
echo "Please enter your NordVPN API token (you can get it from https://my.nordaccount.com/dashboard/nordvpn/access-tokens/):"
read -r token

# Check if token is provided
if [ -z "$token" ]; then
    echo "ERROR: Token cannot be empty"
    exit 1
fi

# Ask if user wants to provide a server hostname
echo "Would you like to specify a server hostname? (y/n)"
read -r specify_server

# Set default server value to empty
server_hostname=""

if [ "$specify_server" == "y" ]; then
    echo "Please enter the server hostname (e.g., gr67.nordvpn.com):"
    read -r server_hostname
fi

# Run Python script with token and optional server hostname
if ! "$PYTHON_CMD" generate_config.py "$token" "$server_hostname"; then
    echo "ERROR: Configuration generation failed"
    exit 1
fi

echo "✅ WireGuard config generated successfully!"
