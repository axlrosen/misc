import csv
import re
import sys

import Levenshtein


# load our dicts
from collections import Counter, defaultdict

RIGHT = re.compile("@.*\n$")

clues = open("/Users/alex.rosen/personal/xword/matt-ginsberg-clues.txt", encoding='latin1').readlines()

clueset = defaultdict(set)
for line in sorted(clues):
    if ("_" in line or "--" in line):
        continue
    parts = line.rstrip().split(",", maxsplit=1)
    clue = parts[1].lower().replace(".", "")
    clue_parts = clue.split(" ")
    if len(clue_parts) != 3:
        continue
    if clue_parts[0] == clue_parts[1]:
        continue
    if clue_parts[0] == clue_parts[2]:
        continue
    if clue_parts[0].endswith("ly") or clue_parts[1].endswith("ly"):
        continue
    if len(set(clue_parts).intersection({"feeling", "feelings", "look", "looks", "or", "and"})) > 0:
        continue
    clueset[(clue_parts[0], clue_parts[1], clue_parts[2])].add(parts[0])
    if (clue_parts[2], clue_parts[1], clue_parts[0]) in clueset:
        print(clue_parts[0], clue_parts[1], clue_parts[2],
              clueset[(clue_parts[0], clue_parts[1], clue_parts[2])],
              clueset[(clue_parts[2], clue_parts[1], clue_parts[0])])

