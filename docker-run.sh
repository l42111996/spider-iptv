#!/bin/sh
set -eu

LOCK_DIR=/tmp/spider-iptv.lock
if ! mkdir "$LOCK_DIR" 2>/dev/null; then
    echo "Another spider-iptv run is already in progress; exiting."
    exit 0
fi
trap 'rmdir "$LOCK_DIR"' EXIT INT TERM

cd /app
python3 main.py

mkdir -p /output
for file in source/iptv.txt source/iptv.m3u; do
    if [ -f "$file" ]; then
        cp -f "$file" /output/
        echo "Exported $file to /output/"
    fi
done
