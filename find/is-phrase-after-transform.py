import re
import Levenshtein


# load our dicts
from collections import Counter, defaultdict

from splitter.wordninja_local import phrase, split_with_cost, split, strict_phrase, loose_phrase

# entries = set()
# wordlist = open("/Users/alex.rosen/personal/xword/dicts/broda-list-03.2020-trimmed-by-diehl.dict").readlines()
# for word in wordlist:
#     entries.add(word.split(';')[0])
from util.pos import is_phrase

wordlist = None
with open('/Users/alex.rosen/personal/projects/misc/splitter/SUBTLEXus74286wordstextversion.txt') as f:
  wordlist = f.read().splitlines()
wordlist = wordlist[1:40000]
wordlist = [e.split()[0].lower() for e in wordlist]
picky_wordlist = set(wordlist[:1000])
wordlist = set(wordlist)

names = set()
ns = open("/Users/alex.rosen/personal/xword/corpora/first-names.txt").readlines()
for n in ns:
    names.add(n.rstrip().lower())


entries = open("/Users/alex.rosen/personal/xword/combined/combined.txt").readlines()
# entries = set(open("/Users/alex.rosen/personal/xword/corpora/wikipedia-4a-stripped.txt").readlines())

WORD = "i"

def is_good_phrase(sp_transformed):
    if len(sp_transformed) > 4:
        return False
    if sp_transformed[0] in {"and", "or", "but"} or sp_transformed[-1] in {"and", "or", "but", "in", "at", "from", "is", "are", "i", "a"}:
        return False
    for w in sp_transformed:
        if w not in wordlist and w not in names:
            return False
        if len(w) == 2 and w not in picky_wordlist:
            return False
        if len(w) == 1 and w not in {"i", "a"}:
            return False
        if w in {"ti", "mi", "il", "lv","ng","vd","fv","de","li","er","en","el","vg","th","es","est", "vl","vrs","vu","sv", "sov", "der", "ivn", "lvio", "vce", "vio", "ves", "vay", "ver", "vers",
                 "ving", "vion", "cve", "vie", "von"}:
            return False
        # if WORD in w:
            # if len(w) == 2 and w not in {"tv", "rv", "av", "vs"}:
            #     return False
    # if sp_transformed[0] == "vs" or sp_transformed[-1] == "vs":
    #     return False
    return True

def move():
    for entry in sorted(list(entries)):
        entry = entry.rstrip()
        if len(entry) <= 15: continue
        if len(entry) > 21: continue
        pos = entry.find(WORD)
        if pos < 0: continue
        if entry.find(WORD, pos+1) >= 0: continue
        zzz = split_with_cost(entry)
        if len(zzz) != 2: continue
        sp, cost = zzz
        sp = list(sp)
        omitted = entry.replace(WORD, "")
        for i in range(0, len(omitted)+1):
            if i == pos: continue
            transformed = omitted[:i] + WORD + omitted[i:]
            if is_phrase(transformed):
                sp_transformed = list(split(transformed))

                # ensure phrases are disjoint
                intersection = set(sp_transformed).intersection(set(sp))
                if intersection and (len(intersection) > 1 or len(intersection.pop()) > 5): continue
                # if intersection: continue

                # if WORD not in sp and WORD not in sp_transformed and len(sp_transformed) <= 3 and not {"xt", "xj", "va", "xg", "xi", "ix"}.intersection(set(sp_transformed)):
                # if WORD in sp or WORD in sp_transformed and len(sp_transformed) <= 3 and not {"xt", "xj", "va", "xg", "xi", "ix"}.intersection(set(sp_transformed)):
                if is_good_phrase(sp_transformed):
                    print(" ".join(sp), "    ", " ".join(split(transformed)))


def remove():
    for entry in sorted(list(entries)):
        entry = entry.rstrip()
        if len(entry) < 9: continue
        pos = entry.find(WORD)
        if pos < 0: continue
        zzz = split_with_cost(entry)
        if len(zzz) != 2: continue
        sp, cost = zzz
        sp = list(sp)
        transformed = entry[0:pos] + entry[pos + len(WORD):]
        if loose_phrase(transformed):
            print(" ".join(sp), "    ", " ".join(split(transformed)))

def contains_intact(phrase, word):
    for p in phrase:
        if p.startswith(word):  # and len(p) <= len(word) + 2:
            return True
    return False


def disjoint(phrase1, entry):
    phrase2 = split(entry)
    for p1 in phrase1:
        for p2 in phrase2:
            if p1 == p2:
                return False

    return True

def add():
    for entry in sorted(list(entries)):
        entry = entry.rstrip()
        if len(entry) < 9: continue
        for pos in range(len(entry)+1):
            transformed = entry[0:pos] + WORD + entry[pos:]
            x = loose_phrase(transformed)
            if x:
                phrase, cost = x
                if not contains_intact(phrase, WORD) and is_good_phrase(phrase) and disjoint(phrase, entry):
                    print(" ".join(split(entry)), "    ", " ".join(phrase))


move()