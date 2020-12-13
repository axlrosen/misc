import re
import Levenshtein


# load our dicts
from collections import Counter, defaultdict

# entries = set()
# broda = open("/Users/alex.rosen/personal/xword/dicts/broda-list-03.2020-trimmed-by-diehl.dict").readlines()
# for word in broda:
#     entries.add(word.split(';')[0])
#
entries = set(open("/Users/alex.rosen/personal/xword/combined/combined.txt").readlines())


with open('/Users/alex.rosen/personal/projects/misc/splitter/SUBTLEXus74286wordstextversion.txt') as f:
  wordlist = f.read().splitlines()
wordlist = wordlist[1:40000]
wordlist = set([e.split()[0].lower() for e in wordlist])


def transform(w: str):
    if not "x" in w: return None
    return w.replace("x","")

orig = []
trans = []
for w in sorted(list(wordlist)):
    if len(w) < 3: continue
    transformed = transform(w)
    if transformed in wordlist:
        print(f"{w}   {transformed}")
        orig.append(w)
        trans.append(transformed)

print("===============================")

for entry in sorted(list(entries)):
    entry = entry.rstrip()
    if len(entry) < 7: continue
    for w1 in range(len(orig)):
        for w2 in range(len(trans)):
            if w1 == w2: continue
            i = entry.find(orig[w1])
            if i >= 0:
                j = entry.find(trans[w2])
                if j >= 0 and j != i+1:
                    t = entry.replace(orig[w1], trans[w1]).replace(trans[w2], orig[w2])
                    print(entry, orig[w1], trans[w2], t)
