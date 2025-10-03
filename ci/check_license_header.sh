#!/usr/bin/env bash

#
# Copyright IBM Corp. All Rights Reserved.
#
# SPDX-License-Identifier: Apache-2.0
#

TARGET_DIR="${1:-.}"

# Expected header
read -r -d '' EXPECTED <<'EOF'
#
# Copyright IBM Corp. All Rights Reserved.
#
# SPDX-License-Identifier: Apache-2.0
#
EOF

status=0

while IFS= read -r -d '' file; do
    # Skip deleted files but still tracked by git
    if [[ -f "$file" ]]; then
        # Read the same number of lines as the expected header
        header=$(head -n "$(echo "$EXPECTED" | wc -l)" "$file")

        if [[ "$header" != "$EXPECTED" ]]; then
            echo "❌ Missing or incorrect header in: $file"
            status=1
        fi
    fi
done < <(
    git -C "$TARGET_DIR" ls-files -z -- '*.yaml' '*.yml' \
    && git -C "$TARGET_DIR" ls-files --others --exclude-standard -z -- '*.yaml' '*.yml'
)

if [[ $status -eq 0 ]]; then
    echo "✅ All YAML files have the correct license header."
else
    echo "Some YAML files are missing the required license header."
    exit 1
fi
