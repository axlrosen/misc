import re
import Levenshtein


# load our dicts
from collections import Counter, defaultdict

entries = set()
clued_words = open("/Users/alex.rosen/personal/xword/dicts/CLUED.dict").readlines()
for word in clued_words:
    entries.add(word.split(';')[0].lower())
xwordinfo_words = open("/Users/alex.rosen/personal/xword/dicts/XwiWordList_autodemoted50to473727_autodemoted25to20.dict").readlines()
for word in xwordinfo_words:
    entries.add(word.split(';')[0])
peter = open("/Users/alex.rosen/personal/xword/dicts/broda-list-03.2020-trimmed-by-diehl.dict", encoding='latin1').readlines()
for word in peter:
    entries.add(word.lower().split(';')[0])
# words = open("/Users/alex.rosen/personal/xword/corpora/most-common-words.txt").readlines()
# for word in words:
#     entries.add(word.lower().rstrip())


for entry in sorted(list(entries)):
    if len(entry) == 9:
        back = entry[::-1]
