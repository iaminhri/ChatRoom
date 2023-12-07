#!/bin/bash

# Checking if pip is installed
if ! command -v pip &> /dev/null; then
    echo "pip not found, installing pip..."
    # Install pip
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python get-pip.py
    rm get-pip.py
fi

pip install termcolor
pip install pwntools

