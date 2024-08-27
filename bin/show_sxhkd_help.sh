#!/bin/bash

SXHKD_CONFIG="$HOME/.config/sxhkd/sxhkdrc"

TEMP_FILE=$(mktemp)

comment=""

while IFS= read -r line; do
    if [[ "$line" =~ ^# ]]; then
        comment="${line/#\# /}"
    elif [[ "$line" =~ ^[[:alnum:]] ]]; then
        echo -e "$comment\n$line\n" >> "$TEMP_FILE"
        comment=""
    fi
done < "$SXHKD_CONFIG"

alacritty -e less "$TEMP_FILE"

rm "$TEMP_FILE"