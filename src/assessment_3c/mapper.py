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

        # friend_id = int(friend.split(':')[0])
        # weight = int(friend.split(':')[1])  # weight is currently not used, but can be included in the output if needed
        # connect_date = friend.split(':')[2]  # connect_date is currently not used, but can be included in the output if needed
        # friend_ids.append(friend_id)

    # Direct friendships
    for friend_id, weight, connect_date in friend_data:
        key = tuple(sorted((user_id, friend_id)))
        value = ("direct", None)
        print(f"{key[0]},{key[1]}\tdirect,0,{location},{weight},{connect_date}")

    # Mutual friendships
    for (friend1, weight, connect_date), (friend2, weight, connect_date)  in combinations(friend_data, 2):
        key = tuple(sorted((friend1, friend2)))
        value = ("mutual", user_id)  # user_id is the mutual friend
        print(f"{key[0]},{key[1]}\tmutual,{user_id},{location},{weight},{connect_date}")
