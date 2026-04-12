#!/usr/bin/env python3
# reducer 2
import sys
import os


SAME_LOCATION_ONLY = os.environ.get('same_location_only', 'false').lower() == 'true'
current_key = None
values = []

def process(key, values):
    recommendations = []
    user_location = None

    for value in values:
        # having some issues with spaces, so stripping them just in case
        parts = [x.strip() for x in value.split(',')]
        recommended_friend = parts[0]
        count = int(parts[1])
        is_direct = int(parts[2])
        location = parts[3]

        if user_location is None:
            user_location = location  # Set user location from the first value

        if is_direct == 1:
            continue  # Skip direct friendships for recommendations

        if SAME_LOCATION_ONLY and location != user_location:
            continue  # Skip if same_location_only is True and locations do not match

        # if is_direct == 0:  # Only consider non-direct friendships for recommendations
        recommendations.append((recommended_friend, count))

    # Sort recommendations by count in descending order and then by recommended friend ID in ascending order
    recommendations.sort(key=lambda x: (-x[1], int(x[0])))

    recommended_friends = [friend for friend, _ in recommendations[:10]]  # Get top 10 recommended friends
    output = ", ".join(recommended_friends) # ignore counts for output

    print(f"{key}\t{output}")

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    key, value = line.split('\t')

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

