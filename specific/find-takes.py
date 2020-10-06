import re
import Levenshtein


# load our dicts
from collections import Counter, defaultdict

entries = set()
broda = open("/Users/alex.rosen/personal/xword/dicts/broda-list-03.2020-trimmed-by-diehl.dict").readlines()
for word in broda:
    entries.add(word.split(';')[0])

TAKES_LIST = {"take", "free" "remove", "steal", "takeout", "pullout", "pull", "delete", "erase", "scrub", "strike"}
taken_list = {}
for entry in entries:
    for take in TAKES_LIST:
        if entry.startswith(take) and len(entry) >= len(take) + 2 and len(entry) <= len(take) + 4 :
            taken_list[entry] = entry[len(take):]

print(sorted(taken_list))

for complete, taken in taken_list.items():
    found = set()
    for entry in entries:
        if len(entry) < 7: continue
        if taken not in entry: continue
        transformed = entry.replace(taken, "")
        if entry.startswith(transformed) or entry.endswith(transformed): continue
        if transformed not in entries: continue
        found.add(entry + ":" + transformed)

    if len(found) < 10: continue

    # result.sort(key=lambda x: (len(x), x))
    # found.sort()
    print(complete)
    print(" ".join(found))
    print()
