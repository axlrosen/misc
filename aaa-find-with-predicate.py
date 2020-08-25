import re
import Levenshtein


# load our dicts
from collections import Counter, defaultdict

broda = open("/Users/alex.rosen/personal/xword/dicts/broda-list-03.2020-trimmed-by-diehl.dict").readlines()
entries = sorted([word.split(';')[0] for word in broda])

buckets = defaultdict(set)


def pred(entry):
    if len(entry) < 7: return False
    for i in range(len(entry) - 6):
        if entry[i] in "ymca": continue
        if entry[i+6] in "ymca": continue
        if not sorted(entry[i+1:i+5]) == ["a", "c", "m", "y"]: continue
        buckets[entry[i+1:i+5]].add(entry)
        return True
    return False

result = [entry for entry in entries if pred(entry)]
result.sort(key=lambda x: (len(x), x))
[print(x) for x in result]

[print("\n" + bucket + "\n" + "\n".join(results)) for bucket, results in buckets.items()]