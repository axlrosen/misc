import re
import Levenshtein


# load our dicts
from collections import Counter, defaultdict

from splitter.wordninja_local import split_with_cost

entries = set([line.rstrip() for line in open("/Users/alex.rosen/personal/xword/combined/combined.txt").readlines()])
entries.add("frenchdressing")
entries.add("billingcycle")

wordlist = None
with open('/Users/alex.rosen/personal/projects/misc/splitter/SUBTLEXus74286wordstextversion.txt') as f:
  wordlist = f.read().splitlines()
wordlist = wordlist[1:40000]
wordlist = [e.split()[0].lower() for e in wordlist]
picky_wordlist = set(wordlist[:1000])
wordlist = set(wordlist)
wordlist.add("frenching")

ns = open("/Users/alex.rosen/personal/xword/corpora/first-names.txt").readlines()
for n in ns:
    wordlist.add(n.rstrip().lower())

for entry in sorted(list(entries)):
    if "ing" not in entry: continue
    if not entry.replace("ing","") in entries:
        zzz = split_with_cost(entry)
        if len(zzz) != 2: continue
        sp, cost = zzz
        sp = list(sp)
        if len(sp) != 2: continue
        if "ing" in sp[0]:
            a = sp[0].replace("ing","")
            b = (sp[1][:-1] if sp[1].endswith("e") else sp[1]) + "ing"
        else:
            a = (sp[0][:-1] if sp[0].endswith("e") else sp[0]) + "ing"
            b = sp[1].replace("ing","")
        if a in wordlist and b in wordlist:
            print(sp[0], sp[1], ": ", a, b)