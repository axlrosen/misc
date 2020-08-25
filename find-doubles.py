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
# words = open("/Users/alex.rosen/personal/xword/corpora/most-common-words.txt").readlines()
# for word in words:
#     entries.add(word.lower().rstrip())

WORD = "room"

roommates = {entry[:-len(WORD)] for entry in entries if len(entry) >= 7 and entry.endswith(WORD)}
roommates -= set(['art', 'house', 'dirty', 'gun', 'spin', 'sales', 'sale', 'ward', 'ladies', 'mens', 'tack', 'one', 'outof', 'sea', 'day', 'the', 'two', 'worka'])
print(roommates)



result = []
for roommate in roommates:
    for roommate2 in roommates:
        if roommate != roommate2 and len(roommate + roommate2) == 13 and (roommate + roommate2) in entries:
            result.append(roommate + " " +roommate2)

# result.sort(key=lambda x: (len(x), x))
result.sort()
[print(x) for x in result]
