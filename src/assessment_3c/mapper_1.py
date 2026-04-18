#!/usr/bin/env python3
# mapper 1
import sys
from itertools import combinations
import os
from datetime import datetime, timedelta

CONNECTED_THIS_YEAR_ONLY = os.environ.get('connected_this_year_only', 'false').lower() == 'true'

def is_recent(date_str):
    try:
        d = datetime.strptime(date_str, '%Y-%m-%d')
        return d >= datetime.now() - timedelta(days=365)
    except:
        return False

for line in sys.stdin:
    friends = line.strip().split("\t")  # split by tab to handle cases where words are separated by tabs
    user_id = int(friends[0].strip())
    location = friends[1].strip()
    friend_list_raw = friends[2].split(',')

    friend_ids = []
    weight = 0
    connect_date = 'unknown'
    friend_data = []

    for friend in friend_list_raw:
        try:
            friend_id, weight, connect_date = friend.split(':')

            friend_id = int(friend_id.strip())
            weight = int(weight.strip())
            connect_date = connect_date.strip()

            # Apply filter
            if CONNECTED_THIS_YEAR_ONLY and not is_recent(connect_date):
                continue

            friend_data.append((friend_id, weight, connect_date))

        except ValueError:
            continue


    # Direct friendships
    for friend_id, weight, connect_date in friend_data:
        print(f"{user_id},{friend_id}\tdirect,0,{weight},{connect_date}")

    # Mutual friendships
    for (friend1, w1,d1), (friend2, w2, d2)  in combinations(friend_data, 2):
        key = tuple(sorted((friend1, friend2)))
        bridge_weight = w1
        bridge_date = d1
        print(f"{key[0]},{key[1]}\tmutual,{user_id},{bridge_weight},{bridge_date}")

    # Dummy record to ensure we have a record for each user in the reducer for location data after filtering
    print(f"{user_id},{user_id}\tdirect,0,0,unknown")
