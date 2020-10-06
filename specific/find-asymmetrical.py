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

def matches_anywhere(entry):
    for i in range(0, len(entry)):
        s = entry[i:]
        result = r.search(s.upper())
        if result and len(result.group(0)) >= 3 and len(result.group(0)) != len(entry):
            return True
    return False


r = re.compile('[eiouy]')
r2 = re.compile('a.*a.*a')


def is_asymetrical(entry):
    if len(entry) < 6: return False
    if r.search(entry): return False
    if not r2.search(entry): return False
    z = len(entry)
    for i in range(z):
        if entry[i] == 'a' and entry[z-i-1] != 'a':
            return False
    return True

result = [entry for entry in entries if is_asymetrical(entry)]
result.sort(key=lambda x: (len(x), x))
[print(x) for x in result]
