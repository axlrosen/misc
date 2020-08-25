import re
import sys

import Levenshtein


# load our dicts
from collections import Counter, defaultdict

from wordninja_local import split, DEFAULT_LANGUAGE_MODEL

entries = set()
clued_words = open("/Users/alex.rosen/personal/xword/dicts/CLUED.dict").readlines()
for word in clued_words:
    entries.add(word.split(';')[0].lower())
xwordinfo_words = open("/Users/alex.rosen/personal/xword/dicts/XwiWordList.dict").readlines()
for word in xwordinfo_words:
    entries.add(word.split(';')[0])
peter = open("/Users/alex.rosen/personal/xword/dicts/peter-broda-wordlist__scored.dict", encoding='latin1').readlines()
for word in peter:
    entries.add(word.lower().split(';')[0])

def score(words):
    total = 0
    mult = 1.0
    count = 0
    for word in words:
        s = DEFAULT_LANGUAGE_MODEL._wordcost.get(word, 100000000)
        if s > 13.5 or "gni" in word: return 1000000000
        if len(word) >= 3 and word not in entries: return 100000000
        total += s
        mult *= s
        count += 1
        # print(word, s, total / count, mult / count, mult ** -count)
    return mult / (1.2**count)



# print(score(split("thisisveryeasy")))
# print()
# print(score(split("extremelygooda")))
# print()
# print(score(split("auiwheaiuhwxef")))
# print()
# print(score(split("zzxvzxcvzvcvzx")))
# sys.exit(0)


def check_one_entry(entry):
    bad_pivot = -1
    real_split = split(entry)
    if len(real_split) == 2 and score(real_split) < 10000:
        bad_pivot = len(real_split[0])

    for i in range(1, len(entry) - 1):
        if i == bad_pivot: continue
        s1 = entry[:i]
        s2 = entry[i:]
        words1 = split(s1 + s1[::-1])
        words2 = split(s2[::-1] + s2)
        if words1[0] == entry or words2[-1] == entry: continue
        total_score = score(words1) * score(words2)
        if total_score < 15000 and len(words1) <= 5 and len(words2) <= 5:
            print(entry, words1, words2, score(words1), score(words2), total_score)


for entry in sorted(entries):
    if len(entry) != 8: continue
    check_one_entry(entry)

