#!/usr/bin/env python3
"""
Bingo card maker for play-along-with-TV

cat list_of_positions | tv_bingo.py > tab_delimited.txt

"""
import random
import sys

entries = set()
for raw in sys.stdin:
    raw = raw.strip()
    if not raw or "#" == raw[0]:
        continue
    entries.add(raw)

for _ in range(4):
    pool = list(entries)
    random.shuffle(pool)

    for l in range(5):
        for c in range(4):
            if pool:
                print(pool.pop(), end="\t")
        if pool:
            print(pool.pop(), end="\n")
    print("\n")
