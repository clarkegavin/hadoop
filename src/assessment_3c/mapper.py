#!/usr/bin/env python3
# mapper 1
import sys
from itertools import combinations


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
            friend_data.append((int(friend_id), int(weight), connect_date))
        except ValueError:
            # Handle cases where the friend data is not in the expected format
            continue

    # Emit User Location
    print(f"{user_id}\tUser_Location,{location}")

    # Direct friendships
    for friend_id, weight, connect_date in friend_data:
        key =  tuple((user_id, friend_id))
        #value = ("direct", None)
        #print(f"{key[0]},{key[1]}\tdirect,0,{location},{weight},{connect_date}")
        print(f"{key[0]},{key[1]}\tdirect,0,{weight},{connect_date}")

    # Mutual friendships
    for (friend1, w1,d1), (friend2, w2, d2)  in combinations(friend_data, 2):
        key = tuple(sorted((friend1, friend2)))
        #value = ("mutual", user_id)  # user_id is the mutual friend
        #print(f"{key[0]},{key[1]}\tmutual,{user_id},unknown,{weight},{connect_date}")
        #print(f"{key[0]},{key[1]}\tmutual,{user_id},{weight},{connect_date}")
        # use the weight of the mutual friend that is connected to the user_id as the weight for the mutual friendship
        bridge_weight = w1 if friend1 == user_id else w2
        bridge_date = d1 if friend1 == user_id else d2

        print(f"{key[0]},{key[1]}\tmutual,{user_id},{bridge_weight},{bridge_date}")
