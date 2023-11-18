
#!/bin/bash

# Function to check for Python installation
check_python() {
    command -v python >/dev/null 2>&1 || command -v python3 >/dev/null 2>&1
    if [ $? -eq 0 ]; then
        PYTHON_CMD=$(command -v python || command -v python3)
        echo "Found Python: $PYTHON_CMD"
    else
        echo "Python not found. Please install Python."
        exit 1
    fi
}

# Check for Python
echo "Checking for Python..."
check_python

# Check and install requirements
$PYTHON_CMD scripts/check_requirements.py requirements.txt
if [ $? -ne 0 ]; then
    echo "Installing missing packages..."
    $PYTHON_CMD -m pip install -r requirements.txt
fi

# Menu for module selection
while true; do
    echo
    echo "Please choose a module to run:"
    echo "1. fincli"
    echo "2. fundainsight"
    echo
    read -p "Enter your choice (1 or 2): " choice

    case $choice in
        1 ) $PYTHON_CMD -m fincli "$@"; break;;
        2 ) $PYTHON_CMD -m fundainsight "$@"; break;;
        * ) echo "Invalid choice. Please choose 1 or 2."
    esac
done

# Optional pause (commented out)
# read -p "Press enter to continue..."
