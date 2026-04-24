#!/usr/bin/env bash

#
# Copyright IBM Corp. All Rights Reserved.
#
# SPDX-License-Identifier: Apache-2.0
#

# Script to check for trailing spaces in Jinja2 template files
# Trailing spaces at the end of lines can cause issues when templating

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# vars
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)
DEFAULT_PROJECT_DIR=$(dirname "${SCRIPT_DIR}")
PROJECT_DIR="${PROJECT_DIR:-$DEFAULT_PROJECT_DIR}"

# Counter for files with issues
files_with_trailing_spaces=0
total_lines_with_trailing_spaces=0

# Find all .j2 files in the project
echo "Checking for trailing spaces in Jinja2 files in: $PROJECT_DIR"
echo ""

# Use find to locate all .j2 files
while IFS= read -r -d '' file; do
    # Check if file has trailing spaces
    if grep -n ' $' "$file" > /dev/null 2>&1; then
        if [ $files_with_trailing_spaces -eq 0 ]; then
            echo -e "${RED}Found files with trailing spaces:${NC}"
            echo ""
        fi
        
        files_with_trailing_spaces=$((files_with_trailing_spaces + 1))
        
        echo -e "${YELLOW}File: $file${NC}"
        
        # Show lines with trailing spaces
        while IFS= read -r line; do
            line_number=$(echo "$line" | cut -d: -f1)
            line_content=$(echo "$line" | cut -d: -f2-)
            echo "  Line $line_number: ${line_content}$"
            total_lines_with_trailing_spaces=$((total_lines_with_trailing_spaces + 1))
        done < <(grep -n ' $' "$file")
        
        echo ""
    fi
done < <(find "$PROJECT_DIR" -type f -name "*.j2" -print0)

# Print summary
echo "----------------------------------------"
if [ $files_with_trailing_spaces -eq 0 ]; then
    echo -e "${GREEN}✓ No trailing spaces found in Jinja2 files${NC}"
    exit 0
else
    echo -e "${RED}✗ Found trailing spaces in $files_with_trailing_spaces file(s)${NC}"
    echo -e "${RED}  Total lines with trailing spaces: $total_lines_with_trailing_spaces${NC}"
    exit 1
fi

