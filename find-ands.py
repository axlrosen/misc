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
# peter = open("/Users/alex.rosen/personal/xword/dicts/peter-broda-wordlist__scored.dict", encoding='latin1').readlines()
# for word in peter:
#     entries.add(word.lower().split(';')[0])
# words = open("/Users/alex.rosen/personal/xword/corpora/most-common-words.txt").readlines()
# for word in words:
#     entries.add(word.lower().rstrip())

pairs = set()
for entry in entries:
    i = entry.find("and")
    if 11 >= len(entry) >= 9 and 2 <= i < len(entry) - 1:
        right = entry[entry.find("and")+3:]
        left = entry[:entry.find("and")]
        if right in entries and left in entries and left != right:
            pairs.add((left, right))

print(sorted(pairs))
pairs = {("over", "out")}

for left, right in pairs:
    leftmates = {entry[:-len(left)] for entry in entries if len(entry) >= 7 and entry.endswith(left)}
    rightmates = {entry[:-len(right)] for entry in entries if len(entry) >= 7 and entry.endswith(right)}

    result = []
    for leftmate in leftmates:
        for rightmate in rightmates:
            if (len(leftmate + rightmate) >= 7 and (leftmate + rightmate) in entries and leftmate != right and rightmate != left):
                result.append(leftmate + " " +rightmate)

    if len(result) < 15: continue

    # result.sort(key=lambda x: (len(x), x))
    result.sort()
    print(left + " and " + right)
    [print(x) for x in result]
    print()
