#!/bin/bash

CHROMIUM_VERSION="129.0.6668.58-1"
DOWNLOAD_URL="https://github.com/ungoogled-software/ungoogled-chromium-portablelinux/releases/download/${CHROMIUM_VERSION}/ungoogled-chromium_${CHROMIUM_VERSION}_linux.tar.xz"
DOWNLOAD_DIR="./chromium"
ARCHIVE_NAME="ungoogled-chromium.tar.xz"

mkdir -p "$DOWNLOAD_DIR"

echo "Downloading Ungoogled Chromium..."
curl -L "$DOWNLOAD_URL" -o "${DOWNLOAD_DIR}/${ARCHIVE_NAME}"

if [ $? -ne 0 ]; then
    echo "Failed to download Ungoogled Chromium. Exiting."
    exit 1
fi

echo "Extracting Ungoogled Chromium..."
tar -xJf "${DOWNLOAD_DIR}/${ARCHIVE_NAME}" -C "$DOWNLOAD_DIR"

if [ $? -ne 0 ]; then
    echo "Failed to extract Ungoogled Chromium. Exiting."
    exit 1
fi

echo "Cleaning up..."
rm "${DOWNLOAD_DIR}/${ARCHIVE_NAME}"

echo "Ungoogled Chromium has been successfully downloaded and extracted to ${DOWNLOAD_DIR}"
