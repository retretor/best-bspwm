#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if cd "$SCRIPT_DIR"; then
    echo "Successfully navigated to script directory: $SCRIPT_DIR"
else
    echo "Error: Failed to navigate to script directory: $SCRIPT_DIR" >&2
    exit 1
fi

echo "Starting installation..."

if python3 Builder/install.py; then
    echo "Installation completed successfully."
else
    echo "Error: Installation failed while executing Builder/install.py" >&2
    exit 1
fi
