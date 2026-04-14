#!/usr/bin/env python3
# reducer 2
import sys
import os
from datetime import datetime, timedelta

SAME_LOCATION_ONLY = os.environ.get('same_location_only', 'false').lower() == 'true'
SORT_BY_WEIGHT = os.environ.get('sort_by_weight', 'false').lower() == 'true'
CONNECTED_THIS_YEAR_ONLY = os.environ.get('connected_this_year_only', 'false').lower() == 'true'

current_key = None
values = []

def process(key, values):
    recommendations = []
    user_location = None
    print(f"DEBUG: Processing user {key} | sort_by_weight={SORT_BY_WEIGHT} | total records={len(values)}",
          file=sys.stderr)

    for value in values:
        # having some issues with spaces, so stripping them just in case
        parts = [x.strip() for x in value.split(',')]
        recommended_friend = parts[0]
        count = int(parts[1])
        is_direct = int(parts[2])
        location = parts[3]
        weight = int(parts[4])
        connected_date = parts[5]

        print(f"DEBUG:   {recommended_friend} | mutual={count} | weight={weight} | direct={is_direct}| location={location} | connected_date={connected_date}",
              file=sys.stderr)

        # convert connected_date to a date object if it's not 'unknown' for easier comparison
        connected_date = connected_date.strip()
        if CONNECTED_THIS_YEAR_ONLY and connected_date != 'unknown':
            try:
                connected_date = datetime.strptime(connected_date, '%Y-%m-%d')
                if connected_date < datetime.now() - timedelta(days=365):
                    continue  # Skip if the connection was not made within the last year
            except ValueError:
                pass  # If the date format is incorrect,  ignore it for filtering

        if user_location is None:
            user_location = location  # Set user location from the first value

        if is_direct == 1:
            continue  # Skip direct friendships for recommendations

        if SAME_LOCATION_ONLY and location != user_location:
            continue  # Skip if same_location_only is True and locations do not match


        # if is_direct == 0:  # Only consider non-direct friendships for recommendations
        sort_value = weight if SORT_BY_WEIGHT else count  # Use weight for sorting if SORT_BY_WEIGHT is True, otherwise use count
        recommendations.append((recommended_friend, sort_value, weight, count))

    # Sort recommendations by count in descending order and then by recommended friend ID in ascending order
    recommendations.sort(key=lambda x: (-x[1], int(x[0])))

    top = [f"{f}({score})" for f, score, w, c in recommendations[:10]]
    print(f"DEBUG: Final top for {key}: {top}", file=sys.stderr)

    recommended_friends = [friend for friend, _,_,_ in recommendations[:10]]  # Get top 10 recommended friends
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

print("DEBUG: Reducer finished successfully", file=sys.stderr)