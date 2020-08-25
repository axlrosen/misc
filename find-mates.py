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

WORD = "mates"

firsthalves = {entry[:-len(WORD)] for entry in entries if len(entry) >= 7 and entry.endswith(WORD)}

for firsthalf in firsthalves:
    secondhalves = {entry[len(firsthalf):] for entry in entries if
                   len(entry) >= 7 and entry.startswith(firsthalf)}
    result = []
    for roommate in secondhalves:
        for roommate2 in secondhalves:
            if roommate != roommate2 and len(roommate + roommate2) >= 7 and (roommate + roommate2) in entries:
                result.append(roommate + " " + roommate2)

    if len(result) > 0:
        # result.sort(key=lambda x: (len(x), x))
        result.sort()
        print(firsthalf + ": " + str(result))
