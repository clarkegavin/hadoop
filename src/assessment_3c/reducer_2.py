#!/usr/bin/env python3
# reducer 2
import sys
import os

SAME_LOCATION_ONLY = os.environ.get('same_location_only', 'false').lower() == 'true'
SORT_BY_WEIGHT = os.environ.get('sort_by_weight', 'false').lower() == 'true'

current_key = None
values = []


def process(key, values):
    recommendations = []

    print(f"DEBUG: Processing user {key} | sort_by_weight={SORT_BY_WEIGHT} | total records={len(values)}",
          file=sys.stderr)

    for value in values:
        # stripping spaces
        parts = [x.strip() for x in value.split(',')]

        if len(parts) < 7:
            print(f"DEBUG: Skipping malformed record for user {key}: {value}", file=sys.stderr)
            continue  # Skip malformed records

        recommended_friend = parts[0]
        count = int(parts[1])
        is_direct = int(parts[2])
        weight = int(parts[3])
        connected_date = parts[4]
        user_location = parts[5]
        friend_location = parts[6]
        bridges = parts[7] if len(parts) > 7 else ""

        print(
            f"DEBUG:  Record for user {key}: recommended_friend={recommended_friend}, count={count}, is_direct={is_direct}, weight={weight}, connected_date={connected_date}, user_location={user_location}, friend_location={friend_location}",
            file=sys.stderr)

        if is_direct == 1:
            continue  # Skip direct friendships for recommendations

        # Location filtering
        if SAME_LOCATION_ONLY:
            if user_location == 'unknown' and friend_location == 'unknown':
                print(
                    f"DEBUG: Skipping {recommended_friend} for user {key} due to location mismatch (friend location: {friend_location}, user location: {user_location})",
                    file=sys.stderr)
                continue
            elif user_location != friend_location:
                print(
                    f"DEBUG: Skipping {recommended_friend} for user {key} due to location mismatch (friend location: {friend_location}, user location: {user_location})",
                    file=sys.stderr)
                continue

        sort_value = weight if SORT_BY_WEIGHT else count  # Use weight for sorting if SORT_BY_WEIGHT is True, otherwise use count
        recommendations.append((recommended_friend, sort_value, bridges, count))

    # sort
    recommendations.sort(key=lambda x: (-x[1], int(x[0])))  # Sort by sort_value in descending order and then by recommended friend ID in ascending order

    output_parts = []
    for friend, score, bridges, count in recommendations[:10]:  # Get top 10 recommendations
        if bridges:
            output_parts.append(f"{friend} (Mutual Friends: {bridges})")
        else:
            output_parts.append(f"{friend}")

    output = "; ".join(output_parts)
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

print("DEBUG: Reducer finished successfully", file=sys.stderr)