#!/usr/bin/env python3
# mapper 2
import sys
import os

SAME_LOCATION_ONLY = os.environ.get('same_location_only', 'false').lower() == 'true'
SORT_BY_WEIGHT = os.environ.get('sort_by_weight', 'false').lower() == 'true'

location_map = {}

try:
    with open("locations.txt") as f:
        for line in f:
            user, location = line.strip().split("\t")
            location_map[user] = location
except Exception as e:
    pass # If the file doesn't exist or can't be read, we just won't have location data

for line in sys.stdin:

    pair, data = line.strip().split("\t")

    count_str, is_direct_str, weight, connected_date = [x.strip() for x in data.split(',')]
    count = int(count_str)
    is_direct = int(is_direct_str)

    user, recommended_friend = [x.strip() for x in pair.split(',')]

    user_location = location_map.get(user, 'unknown')
    friend_location = location_map.get(recommended_friend, 'unknown')

    print(f"{user}\t{recommended_friend},{count},{is_direct},{weight},{connected_date},{user_location},{friend_location}")
    print(f"{recommended_friend}\t{user},{count},{is_direct},{weight},{connected_date},{friend_location},{user_location}")
