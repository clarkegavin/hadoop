#!/usr/bin/env python3
import sys
from itertools import combinations


for line in sys.stdin:
    friends = line.strip().split("\t")  # split by tab to handle cases where words are separated by tabs

    user_id = int(friends[0].strip())
    location = friends[1].strip()
    friend_list_raw = friends[2].split(',')

    # split friend_list by colon to get individual friends, weight and timestamp
    # friend_list = friend_list_raw.strip().split(',')

    friend_ids = []

    # print(f"{user_id}: {friend_list}")
    for friend in friend_list_raw:
        friend_id = int(friend.split(':')[0])
        friend_ids.append(friend_id)

    # Direct friendships
    for friend_id in friend_ids:
        key = tuple(sorted((user_id, friend_id)))
        value = ("direct", None)
        #print(f"{key}\t{value}")
        print(f"{key[0]},{key[1]}\tdirect,0")

    # Mutual friendships
    for friend1, friend2 in combinations(friend_ids, 2):
        key = tuple(sorted((friend1, friend2)))
        value = ("mutual", user_id)  # user_id is the mutual friend
        #print(f"{key}\t{value}")
        print(f"{key[0]},{key[1]}\tmutual,{user_id}")
