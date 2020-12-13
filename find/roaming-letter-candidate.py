import re
import sys

import Levenshtein
from collections import Counter, defaultdict
import nltk
import wordninja


HOMONYMS_LIST = {"VERB", "NOUN"}
pos = open("/Users/alex.rosen/personal/xword/combined/pos.txt").readlines()
homonyms = [line.split()[0] for line in pos if all(h in line for h in HOMONYMS_LIST)]
homonyms = [h for h in homonyms if len(h) >= 3]

# broda = open("/Users/alex.rosen/personal/xword/dicts/broda-list-03.2020-trimmed-by-diehl.dict").readlines()
# entries = sorted([word.split(';')[0] for word in broda])


combined = open("/Users/alex.rosen/personal/xword/combined/combined15.txt").readlines()
entries = sorted([word.rstrip() for word in combined])
entries_set = set(entries)

def pred(entry):
    if len(entry) < 10: return
    for h in homonyms:
        if entry.endswith(h):
            print(entry, h)

for entry in entries:
    pred(entry)

