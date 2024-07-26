#!/bin/bash

# Function to check if Python is installed
check_python() {
    if command -v python3 &>/dev/null; then
        echo "Python is already installed."
    else
        echo "Python is not installed. Installing Python..."
        
        echo "Please select your distribution:"
        echo "1) Fedora"
        echo "2) Arch"
        echo "3) Debian/Ubuntu"
        read -p "Enter the number corresponding to your distribution: " distro_choice
        
        case "$distro_choice" in
            1)
                echo "Installing Python using dnf for Fedora..."
                sudo dnf install -y python3 python3-virtualenv python3-pip
                ;;
            2)
                echo "Installing Python using pacman for Arch..."
                sudo pacman -Sy --noconfirm python python-virtualenv python-pip
                ;;
            3)
                echo "Installing Python using apt-get for Debian/Ubuntu..."
                sudo apt-get update
                sudo apt-get install -y python3 python3-venv python3-pip
                ;;
            *)
                echo "Invalid selection. Exiting."
                exit 1
                ;;
        esac
    fi
}


# Function to create a virtual environment, install packages, run the script, and delete the environment
run_script() {
    echo "Creating virtual environment..."
    python3 -m venv venv

    echo "Activating virtual environment..."
    source venv/bin/activate

    echo "Installing required packages..."
    pip install requests tqdm zipfile

    echo "Running the script..."
    python3 Linux_Downgrader.py

    echo "Deactivating and removing virtual environment..."
    deactivate
    rm -rf venv
}

# Main script execution
check_python
run_script

echo "Script execution completed."