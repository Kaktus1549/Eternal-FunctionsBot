#!/bin/bash

# Function to install dependencies
install_dependencies() {
    echo "Installing dependencies..."
    pip3 install --upgrade -r requirements.txt
    echo "Dependencies installed successfully."
}

# Function to compile the Python program to a binary
compile_program() {
    echo "Compiling the Python program..."
    python3 -m PyInstaller --onefile FunctionBot.py
    echo "Compilation completed."
}

# Function to remove unnecessary build files
remove_build_files() {
    mv ./dist/FunctionBot ./FunctionBot
    echo "Removing unnecessary build files..."
    rm -rf build dist 
    rm FunctionBot.spec
    echo "Build files removed."
}

# Main script execution
echo "============> Installing dependencies for Function bot! <============"
echo ""
install_dependencies

# Prompt user to compile the program to a binary
read -p "Do you want to compile the program to a binary? (y/n): " compile_choice
if [[ $compile_choice =~ ^[Yy]$ ]]; then
    compile_program
    remove_build_files
fi

echo "Func bot setup completed!"