#!/bin/bash

# Create the browsers directory if it doesn't exist
mkdir -p browsers

# Set the Chrome version as a variable
chrome_version="131.0.6724.0"

# Declare an array of Chrome URLs
chrome_urls=(
    "https://storage.googleapis.com/chrome-for-testing-public/$chrome_version/linux64/chrome-linux64.zip"
    "https://storage.googleapis.com/chrome-for-testing-public/$chrome_version/mac-arm64/chrome-mac-arm64.zip"
    "https://storage.googleapis.com/chrome-for-testing-public/$chrome_version/mac-x64/chrome-mac-x64.zip"
    "https://storage.googleapis.com/chrome-for-testing-public/$chrome_version/win32/chrome-win32.zip"
    "https://storage.googleapis.com/chrome-for-testing-public/$chrome_version/win64/chrome-win64.zip"
)

# Declare an array of ChromeDriver URLs
chromedriver_urls=(
    "https://storage.googleapis.com/chrome-for-testing-public/$chrome_version/linux64/chromedriver-linux64.zip"
    "https://storage.googleapis.com/chrome-for-testing-public/$chrome_version/mac-arm64/chromedriver-mac-arm64.zip"
    "https://storage.googleapis.com/chrome-for-testing-public/$chrome_version/mac-x64/chromedriver-mac-x64.zip"
    "https://storage.googleapis.com/chrome-for-testing-public/$chrome_version/win32/chromedriver-win32.zip"
    "https://storage.googleapis.com/chrome-for-testing-public/$chrome_version/win64/chromedriver-win64.zip"
)

# Function to display options and get user choice
choose_option() {
    echo "Choose which Chrome and ChromeDriver to download:"
    echo "1. Linux 64-bit"
    echo "2. macOS ARM64"
    echo "3. macOS x64"
    echo "4. Windows 32-bit"
    echo "5. Windows 64-bit"
    echo "6. All"
    read -p "Enter your choice (1-6): " choice
    echo
    return $choice
}

# Function to download files
download_files() {
    local chrome_url="$1"
    local chromedriver_url="$2"
    
    echo "Downloading Chrome from $chrome_url..."
    curl -L "$chrome_url" -o "browsers/$(basename $chrome_url)"
    
    echo "Downloading ChromeDriver from $chromedriver_url..."
    curl -L "$chromedriver_url" -o "browsers/$(basename $chromedriver_url)"
}

# Main script
choose_option
choice=$?

case $choice in
    1|2|3|4|5)
        index=$((choice - 1))
        download_files "${chrome_urls[$index]}" "${chromedriver_urls[$index]}"
        ;;
    6)
        for i in "${!chrome_urls[@]}"; do
            download_files "${chrome_urls[$i]}" "${chromedriver_urls[$i]}"
        done
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac

echo "Downloads completed."
