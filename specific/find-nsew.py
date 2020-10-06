import re
import Levenshtein


# load our dicts
from collections import Counter, defaultdict

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
# words = open("/Users/alex.rosen/personal/xword/corpora/famous-people-nndb.txt").readlines()
# for word in words:
#     entries.add(word.lower().rstrip())

entries = sorted(entries)

NEWS = set(['n', 'e', 'w', 's'])
def is_asymetrical(entry):
    if len(entry) < 8 or len(entry) > 17 or "new" in entry or "answer" in entry: return False
    # for pattern in ['nesw', 'nswe', 'wsne', 'ensw', 'wens', 'snew']:
    #     if pattern in entry: return False
    for i in range(1, len(entry) - 4):
        s = set(entry[i:i+4])
        if s == NEWS and entry[i-1] not in "news" and entry[i+4] not in "news":
            return f"{entry[i:i+4].upper()}: {entry} ({len(entry)})"
    return False

for entry in entries:
    x = is_asymetrical(entry)
    if x:
        print(x)

