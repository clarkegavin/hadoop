#!/usr/bin/env python3
# mapper 0
import sys

for line in sys.stdin:
    parts = line.strip().split("\t")
    if len(parts) < 2:
        continue  # Skip malformed lines

    user_id = parts[0].strip()
    location = parts[1].strip()

    print(f"{user_id}\t{location}")