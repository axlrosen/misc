import re
import Levenshtein


# load our dicts
from collections import Counter, defaultdict

entries = set()
broda = open("/Users/alex.rosen/personal/xword/dicts/broda-list-03.2020-trimmed-by-diehl.dict").readlines()
for word in broda:
    entries.add(word.split(';')[0])


regex = re.compile("c.*d")
def transform(w: str):
    if w.endswith("es"):
        return w + "t"
    return None

for entry in entries:
    if len(entry) < 7: continue
    transformed = transform(entry)
    if transformed in entries:
        print(f"{entry}   {transformed}")
