#!/bin/bash

source_dir="/home/simon/.shell_files/bash_files"
target_dir="/usr/local/bin"

# Navigate to the source directory
cd "$source_dir" || exit

# Loop through each file in the source directory
for file in *; do
    # Check if the item is a regular file (not a directory)
    if [ -f "$file" ]; then
        # Create a symbolic link in the target directory with the same filename
        ln -s "$(realpath "$file")" "$target_dir/$file"
    fi
done
