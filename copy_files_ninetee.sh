#!/bin/bash

# Define source and destination directories
SOURCE_DIR="../trainning_tesstain/tesstrain/data/nineteenNinetySeven-ground-truth"
DEST_DIR="train_nineteen"

# Create destination directory if it doesn't exist
mkdir -p "$DEST_DIR"

# Copy files using find and cpio
cd "$SOURCE_DIR"
find . -type f -print | cpio -pdm /path/to/train_new_font/"$DEST_DIR"

echo "Files copied successfully."

