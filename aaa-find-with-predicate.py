import re
import Levenshtein


# load our dicts
from collections import Counter, defaultdict

broda = open("/Users/alex.rosen/personal/xword/dicts/broda-list-03.2020-trimmed-by-diehl.dict").readlines()
entries = sorted([word.split(';')[0] for word in broda])

r = re.compile('[news]')

def pred(entry):
    if len(entry) < 12: return False
    if len(r.findall(entry)) < 4:
        return False
    if "w" in entry or "e" in entry:
        return False
    entry = str(entry)
    length = len(entry)
    i = 0
    while i < length:
        c = entry[i]
        if c == 'n' or c == 's':
            if i == length - 1:
                return False
            if entry[i+1] in "news":
                return False
            if c == 'n' and entry[i+1] in "dgzkyftcvj":
                return False
            length -= 1
            entry = entry[:i+1] + entry[i+2:]
        if c == 'e':
            if i >= length - 2:
                return False
            if entry[i+1] != entry[i+2]:
                return False
            if entry[i+1] in "news":
                return False
            length -= 1
            entry = entry[:i+1] + entry[i+2:]
        if c == 'w':
            if i == 0 or i == length - 1:
                return False
            if entry[i+1] != entry[i-1]:
                return False
            if entry[i+1] in "news":
                return False
            length -= 1
            entry = entry[:i+1] + entry[i+2:]
        i += 1
    return True

result = [entry for entry in entries if pred(entry)]
result.sort(key=lambda x: (len(x), x))
[print(x) for x in result]
