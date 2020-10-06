import re
import Levenshtein


# load our dicts
from collections import Counter, defaultdict

entries = set()
broda = open("/Users/alex.rosen/personal/xword/dicts/broda-list-03.2020-trimmed-by-diehl.dict").readlines()
for word in broda:
    entries.add(word.split(';')[0])


regex = re.compile(r"^(pri)")
def transform(w: str):
    match = regex.search(w)
    if match and not match.group(1) == "ing":
        x =  w[:match.start(1)] + w[match.end(1):]
        # print(w, x)
        return x
    return None

for entry in sorted(list(entries)):
    if len(entry) < 7: continue
    transformed = transform(entry)
    if transformed in entries:
        print(f"{entry}   {transformed}")
