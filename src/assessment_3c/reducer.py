#!/usr/bin/env python3
import sys
# reducer
current_key = None
values = []

def process(key, values):
    has_direct = False
    mutual_friends = []
    location = 'unknown'  # default location if not found
    weight = 0  # default weight if not found
    connect_date = 'unknown'  # default connect_date if not found

    for value in values:
        parts = value.split(',')
        #tag, user_id  = value.split(',')
        tag = parts[0].strip()
        user_id = parts[1].strip()
        weight = parts[3].strip() if len(parts) > 3 else '0'  # update weight if provided
        connect_date = parts[4].strip() if len(parts) > 4 else 'unknown'  # update connect_date if provided
        if tag == "direct":
            has_direct = True
        elif tag == "mutual":
            mutual_friends.append(int(user_id))

        if len(parts) > 2:
            location = parts[2].strip()  # update location if provided

    is_direct_flag = 1 if has_direct else 0
    print(f"{key}\t{len(mutual_friends)},{is_direct_flag},{location},{weight},{connect_date}")

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




