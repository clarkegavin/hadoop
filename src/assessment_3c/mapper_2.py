#!/usr/bin/env python3
# mapper 2
import sys
import os

SAME_LOCATION_ONLY = os.environ.get('same_location_only', 'false').lower() == 'true'
SORT_BY_WEIGHT = os.environ.get('sort_by_weight', 'false').lower() == 'true'
CONNECTED_THIS_YEAR_ONLY = os.environ.get('connected_this_year_only', 'false').lower() == 'true'

for line in sys.stdin:

    pair, data = line.strip().split("\t")
    #having some issues with spaces so stripping them just in case
    count_str, is_direct_str, location, weight, connected_date = [x.strip() for x in data.split(',')]
    count = int(count_str)
    is_direct = int(is_direct_str)

    user, recommended_friend = [x.strip() for x in pair.split(',')]

    print(f"{user}\t{recommended_friend},{count},{is_direct},{location},{weight},{connected_date}")
    print(f"{recommended_friend}\t{user},{count},{is_direct},{location},{weight},{connected_date}")