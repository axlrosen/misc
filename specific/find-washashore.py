import re
import Levenshtein


# load our dicts
from collections import Counter, defaultdict

entries = set()
# clued_words = open("/Users/alex.rosen/personal/xword/dicts/CLUED.dict").readlines()
# for word in clued_words:
#     entries.add(word.split(';')[0].lower())
xwordinfo_words = open("/Users/alex.rosen/personal/xword/dicts/XwiWordList.dict").readlines()
for word in xwordinfo_words:
    entries.add(word.split(';')[0])
peter = open("/Users/alex.rosen/personal/xword/dicts/peter-broda-wordlist__scored.dict", encoding='latin1').readlines()
for word in peter:
    entries.add(word.lower().split(';')[0])
words = set(open("/Users/alex.rosen/personal/xword/corpora/most-common-words.txt").read().splitlines())
# for word in words:
#     entries.add(word.lower().rstrip())

empty = []

def xxx(entry):
    if len(entry) < 3: return empty
    if entry[0] != 'a': return empty
    tail = entry[1:]
    if tail == 'shore':
        print(tail in words)
    if tail not in words: return empty
    x = [e for e in entries if e.endswith(entry)]
    print(entry, x)


result = [xxx(entry) for entry in entries]
result = [item for items in result for item in items]
result.sort(key=lambda x: (len(x), x))
[print(x) for x in result]
