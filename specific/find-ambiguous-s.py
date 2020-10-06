import re
import Levenshtein


# load our dicts
from collections import Counter, defaultdict

entries = set()
xwordinfo_words = open("/Users/alex.rosen/personal/xword/dicts/broda-list-03.2020-trimmed-by-diehl.dict").readlines()
for word in xwordinfo_words:
    entries.add(word.split(';')[0])


for entry in entries:
    if len(entry) < 7: continue
    i = 4
    while True:
        i = entry.find("s", i+1, -4)
        if i < 0: break
        before = entry[:i]
        after = entry[i+1:]
        if before in entries and after in entries:
            print(f"{before}'s {after}")
