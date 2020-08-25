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

def matches_anywhere(entry):
    for i in range(0, len(entry)):
        s = entry[i:]
        result = r.search(s.upper())
        if result and len(result.group(0)) >= 3 and len(result.group(0)) != len(entry):
            return True
    return False


# r = re.compile('^[^MDCLXVI]*(?=[MDCLXVI])M*(C[MD]|D?C{0,3})(X[CL]|L?X{0,3})(I[XV]|V?I{0,3})[^MDCLXVI]*$')
r = re.compile('(?=[MDCLXVI])M*(C[MD]|D?C{0,3})(X[CL]|L?X{0,3})(I[XV]|V?I{0,3})')
for entry in entries:
    if len(entry) != 7: continue
    if matches_anywhere(entry):
    # if result and len(result.group(0)) >= 4 and len(result.group(0)) != len(entry):
    # if result and len(result.group(0)) == 3 and len(result.group(0)) != len(entry) and "cl" not in entry.lower() and "v" not in entry.lower():
        print(entry)

