import re
import Levenshtein


# load our dicts
from collections import Counter, defaultdict

broda = open("/Users/alex.rosen/personal/xword/dicts/broda-list-03.2020-trimmed-by-diehl.dict").readlines()
entries = sorted([word.split(';')[0] for word in broda])

buckets = defaultdict(set)


def pred(entry):
    if len(entry) < 7: return False
    return len(set(entry[-5:])) == 2 and not entry.endswith("es")

result = [entry for entry in entries if pred(entry)]
result.sort(key=lambda x: (len(x), x))
[print(x) for x in result]

