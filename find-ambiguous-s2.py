import re
import Levenshtein


# load our dicts
from collections import Counter, defaultdict

entries = set()
clued_words = open("/Users/alex.rosen/personal/xword/dicts/split15.txt").readlines()
for word in clued_words:
    entries.add(word.split('/')[1])

names = set()
ns = open("/Users/alex.rosen/personal/xword/corpora/first-names.txt").readlines()
for n in ns:
    names.add(n.rstrip().lower())


for entry in entries:
    if len(entry) < 7: continue
    i = entry.rfind(' s')
    before = entry[:i]
    after = entry[i+2:]
    if before in names and after in entries:
        print(f"{before}'s {after}")
