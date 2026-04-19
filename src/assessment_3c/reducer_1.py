#!/usr/bin/env python3
import sys
# reducer 1
current_key = None
values = []

def process(key, values):
    has_direct = False
    mutual_bridges = set() #store mutual friend id's
    best_weight = 0  # to track the best weight among mutual friends
    connect_date = 'unknown'  # default connect_date if not found

    for value in values:
        parts = value.split(',')
        tag = parts[0].strip()
        user_id = parts[1].strip()
        connect_date = parts[3].strip() if len(parts) > 3 else 'unknown'  # update connect_date if provided

        if tag == "direct":
            has_direct = True
            if len(parts) > 3:
                try:
                    weight = int(parts[2].strip())
                    if weight > best_weight:
                        best_weight = weight
                        connect_date = parts[3].strip()
                except:
                    pass

        elif tag == "mutual":
            try:
                bridge_user = int(parts[1].strip())  # the user who connects them
                weight = int(parts[2].strip())
                mutual_bridges.add(bridge_user)
                if weight > best_weight:
                    best_weight = weight
                    connect_date = parts[3].strip()
            except:
                pass

    is_direct_flag = 1 if has_direct else 0
    bridges_str = ",".join(map(str, sorted(mutual_bridges))) if mutual_bridges else ""

    print(f"{key}\t{len(mutual_bridges)},{is_direct_flag},{best_weight},{connect_date},{bridges_str}")

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




