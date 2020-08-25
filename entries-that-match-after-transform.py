import csv
import re
import sys

import Levenshtein


# load our dicts
from collections import Counter, defaultdict

def transform(entry):
    return "s" + entry

RE = re.compile("^(.*);")

entries_list = open("/Users/alex.rosen/personal/xword/dicts/broda-list-03.2020-trimmed-by-diehl.dict", encoding='latin1').readlines()

entries = set()
for line in entries_list:
    match = RE.search(line.rstrip())
    if not match: continue
    entries.add(match.group(1))

for entry in sorted(list(entries)):
    t = transform(entry)
    if len(t) < 10: continue
    if t in entries:
        print(t)
