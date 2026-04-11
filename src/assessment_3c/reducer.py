#!/usr/bin/env python3
import sys

current_key = None
values = []

def process(key, values):
    has_direct = False
    mutual_friends = []

    for value in values:
        tag, user_id  = value.split(',')
        if tag == "direct":
            has_direct = True
        elif tag == "mutual":
            mutual_friends.append(int(user_id))

    # if there is no direct friendship, output the key and the number of mutual friends
    if not has_direct:
        print(f"{key}\t{len(mutual_friends)}")

for line in sys.stdin:
    key, value = line.strip().split('\t')

    if current_key == key:
        values.append(value)
    else:
        if current_key is not None:
            process(current_key, values)
        current_key = key
        values = [value]

# process the last key
if current_key is not None:
    process(current_key, values)




