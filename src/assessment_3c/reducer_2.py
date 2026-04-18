#!/usr/bin/env python3
# reducer 2
import sys
import os



SAME_LOCATION_ONLY = os.environ.get('same_location_only', 'false').lower() == 'true'
SORT_BY_WEIGHT = os.environ.get('sort_by_weight', 'false').lower() == 'true'
#CONNECTED_THIS_YEAR_ONLY = os.environ.get('connected_this_year_only', 'false').lower() == 'true'

current_key = None
values = []
#user_locations = {}

def process(key, values):
    recommendations = []

    print(f"DEBUG: Processing user {key} | sort_by_weight={SORT_BY_WEIGHT} | total records={len(values)}",
          file=sys.stderr)

    # for value in values:
    #     parts = [x.strip() for x in value.split(',')]
    #     if len(parts) < 2:
    #         print(f"DEBUG: XXX - Skipping malformed record for user {key}: {value}", file=sys.stderr)
    #         continue  # Skip malformed records
    #
    #     if parts[0] == "User_Location":
    #         user_locations[key] = parts[1]  # Store user location for later use
    #         print(f"DEBUG: Found location for user {key}: {user_locations[key]}", file=sys.stderr)
    #
    # print(f"DEBUG: Known locations after collection: {user_locations}", file=sys.stderr)

    for value in values:
        # stripping spaces
        parts = [x.strip() for x in value.split(',')]

        if len(parts) < 6:
            print(f"DEBUG: Skipping malformed record for user {key}: {value}", file=sys.stderr)
            continue  # Skip malformed records

        # if parts[0] == "User_Location":
        #     continue  # Skip user location records in this loop, they are already processed

        recommended_friend = parts[0]
        count = int(parts[1])
        is_direct = int(parts[2])
        weight = int(parts[3])
        connected_date = parts[4]
        user_location = parts[5]
        friend_location = parts[6]

        # user_locations[key] = user_locations.get(key, 'unknown')
        # user_locations[recommended_friend] = user_locations.get(recommended_friend, 'unknown')


        print(
            f"DEBUG:  Record for user {key}: recommended_friend={recommended_friend}, count={count}, is_direct={is_direct}, weight={weight}, connected_date={connected_date}, user_location={user_location}, friend_location={friend_location}",
            file=sys.stderr)

        if is_direct == 1:
            continue  # Skip direct friendships for recommendations

        # convert connected_date to a date object if it's not 'unknown' for easier comparison
        # connected_date = connected_date.strip()
        # if CONNECTED_THIS_YEAR_ONLY and connected_date != 'unknown':
        #     try:
        #         connected_date = datetime.strptime(connected_date, '%Y-%m-%d')
        #         if connected_date < datetime.now() - timedelta(days=365):
        #             continue  # Skip if the connection was not made within the last year
        #     except ValueError:
        #         pass  # If the date format is incorrect,  ignore it for filtering

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
        #recommendations.append((recommended_friend, sort_value, weight, count))
        recommendations.append((recommended_friend, sort_value))

    # sort
    recommendations.sort(key=lambda x: (-x[1], int(x[0])))  # Sort by sort_value in descending order and then by recommended friend ID in ascending order

    top = [friend for friend, score in recommendations[:10]]  # Get top 10 recommended friends
    output = ", ".join(top)  # Join top recommended friends into a comma-separated string

    print(f"DEBUG: Top recommendations for user {key}: {output}", file=sys.stderr)


    # location filtering if SAME_LOCATION_ONLY is enabled
    # final_recommendations = []
    # user_location = user_locations.get(key, 'unknown')
    #
    # for friend, score, weight, count in recommendations:
    #     friend_location = user_locations.get(friend, 'unknown')
    #     print(f"DEBUG:   Friend {friend} location: {friend_location} | User  location: {user_location}", file=sys.stderr)
    #
    #     if SAME_LOCATION_ONLY:
    #         if friend_location == 'unknown' and user_location == 'unknown':
    #             print(
    #                 f"DEBUG:   Skipping {friend} for user {key} due to location mismatch (friend location: {friend_location}, user location: {user_location})",
    #                 file=sys.stderr)
    #             continue
    #         elif friend_location != user_location:
    #             print(
    #                 f"DEBUG:   Skipping {friend} for user {key} due to location mismatch (friend location: {friend_location}, user location: {user_location})",
    #                 file=sys.stderr)
    #             continue
    #
    #     #final_recommendations.append((friend, score, weight, count ))  # Keep the original sort value, weight, and count for sorting
    #     final_recommendations.append(
    #         (friend, score))  # Keep the original sort value, weight, and count for sorting
    #
    # #recommendations = [rec for rec in recommendations if rec[0] != friend]  # Remove this friend from recommendations
    #
    # # Sort recommendations by count in descending order and then by recommended friend ID in ascending order
    # final_recommendations.sort(key=lambda x: (-x[1], int(x[0])))
    #
    # top = [f"{f}({score})" for f, score in final_recommendations[:10]]
    # print(f"DEBUG: Final top for {key}: {top}", file=sys.stderr)
    #
    # top_10_recommended_friends = [friend for friend,score in final_recommendations[:10]]  # Get top 10 recommended friends
    # output = ", ".join(top_10_recommended_friends) # ignore counts for output

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