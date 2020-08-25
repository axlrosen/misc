import csv
import re
import sys

import Levenshtein


# load our dicts
from collections import Counter, defaultdict

RE = re.compile("/([a-z ]*)")

entries_list = open("/Users/alex.rosen/personal/xword/combined/split-peter.txt", encoding='latin1').readlines()

entries = set()
for line in entries_list:
    match = RE.search(line.rstrip())
    if not match: continue
    parts = tuple(match.group(1).split(" "))
    if len(parts) < 3: continue
    # if len(parts[0]) + len(parts[1]) != 8: continue
    # if len(parts[0]) < 4: continue
    if parts in entries:
        continue
    r = tuple(reversed(parts))
    # if r in entries:
    #     print(" ".join(parts))
    if len(set(parts).intersection({"feeling", "feelings", "look", "looks", "or", "and", "hundred"})) > 0:
        continue
    entries.add(parts)

# sys.exit(0)

RE = re.compile("^(.*)_\(")

entries_list = open("/Users/alex.rosen/personal/xword/corpora/wikipedia-4a.txt", encoding='latin1').readlines()

# entries = set()
for line in entries_list:
    parts = line.lower().split(" ")
    match = RE.search(parts[0])
    if match:
        parts[0] = match.group(1)
    parts = tuple(parts[0].split("_"))
    if len(parts) < 3: continue
    if parts in entries:
        continue
    r = tuple(reversed(parts))
    # if r in entries:
    #     print(" ".join(parts))
    if len(set(parts).intersection({"feeling", "feelings", "look", "looks", "or", "and", "hundred"})) > 0:
        continue
    entries.add(parts)


RIGHT = re.compile("@.*\n$")

clues = open("/Users/alex.rosen/personal/xword/matt-ginsberg-clues.txt", encoding='latin1').readlines()

clueset = defaultdict(set)
for line in sorted(clues):
    if ("_" in line or "--" in line):
        continue
    parts = line.rstrip().split(",", maxsplit=1)
    clue = parts[1].lower().replace(".", "")
    parts = tuple(clue.split(" "))
    if len(parts) < 3: continue
    if parts in entries:
        continue
    r = tuple(reversed(parts))
    if r in entries:
        print(" ".join(parts))
    if len(set(parts).intersection({"feeling", "feelings", "look", "looks", "or", "and", "hundred"})) > 0:
        continue
    # entries.add(parts)
