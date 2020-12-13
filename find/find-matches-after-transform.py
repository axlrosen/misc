import gc
import re
from random import randrange

import Levenshtein

# load our dicts
from collections import Counter, defaultdict

# entries = set()
# broda = open("/Users/alex.rosen/personal/xword/dicts/broda-list-03.2020-trimmed-by-diehl.dict").readlines()
# for word in broda:
#     entries.add(word.split(';')[0])
#
# entries = set(open("/Users/alex.rosen/personal/xword/combined/combined.txt").readlines())


# with open('/Users/alex.rosen/personal/projects/misc/splitter/SUBTLEXus74286wordstextversion.txt') as f:
#   wordlist = f.read().splitlines()
# wordlist = wordlist[1:20000]
# wordlist = set([e.split()[0].lower() for e in wordlist])


def transform(w: str):
    if w.startswith("cr"): return None
    return w[2:]

count = 0
entries = sorted(open("/Users/alex.rosen/personal/xword/combined/combined.txt").readlines())
entries = [e.rstrip() for e in entries]
for entry in entries:
    if entry.startswith("cr") and entry[2:] in entries:
        print(entry)
