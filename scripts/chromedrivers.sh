#!/bin/bash

mkdir -p chromedrivers

chromedriver_version="129.0.6668.70"

chromedriver_urls=(
    "https://storage.googleapis.com/chrome-for-testing-public/$chrome_version/linux64/chromedriver-linux64.zip"
    "https://storage.googleapis.com/chrome-for-testing-public/$chrome_version/mac-arm64/chromedriver-mac-arm64.zip"
    "https://storage.googleapis.com/chrome-for-testing-public/$chrome_version/mac-x64/chromedriver-mac-x64.zip"
    "https://storage.googleapis.com/chrome-for-testing-public/$chrome_version/win32/chromedriver-win32.zip"
    "https://storage.googleapis.com/chrome-for-testing-public/$chrome_version/win64/chromedriver-win64.zip"
)

choose_option() {
    echo "Choose which ChromeDriver to download:"
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

download_files() {
    local chromedriver_url="$1"

    echo "Downloading ChromeDriver from $chromedriver_url..."
    curl -L "$chromedriver_url" -o "chrome/$(basename $chromedriver_url)"
}

choose_option
choice=$?

case $choice in
    1|2|3|4|5)
        index=$((choice - 1))
        download_files "${chromedriver_urls[$index]}"
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
