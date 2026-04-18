#!/usr/bin/env python3
# reducer 0
import sys

seen = set()

for line in sys.stdin:
    # deduplication logic: only print the line if we haven't seen it before
    if line not in seen:
        print(line.strip())
        seen.add(line)