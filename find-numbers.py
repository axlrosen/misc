import re
import sys

import Levenshtein


# load our dicts
from collections import Counter, defaultdict

entries = set()
# clued_words = open("/Users/alex.rosen/personal/xword/dicts/CLUED.dict").readlines()
# for word in clued_words:
#     entries.add(word.split(';')[0].lower())
# xwordinfo_words = open("/Users/alex.rosen/personal/xword/dicts/XwiWordList.dict").readlines()
# for word in xwordinfo_words:
#     entries.add(word.split(';')[0])
peter = open("/Users/alex.rosen/personal/xword/dicts/broda-list-03.2020-trimmed-by-diehl.dict", encoding='latin1').readlines()
for word in peter:
    entries.add(word.lower().split(';')[0])


# clued_words = open("/Users/alex.rosen/personal/xword/dicts/CLUED.dict").readlines()
# for word in clued_words:
#     entries.add(word.split(';')[0].lower())
# xwordinfo_words = open("/Users/alex.rosen/personal/xword/dicts/XwiWordList.dict").readlines()
# for word in xwordinfo_words:
#     entries.add(word.split(';')[0])
# peter = open("/Users/alex.rosen/personal/xword/dicts/peter-broda-wordlist__scored.dict", encoding='latin1').readlines()
# for word in peter:
#     entries.add(word.lower().split(';')[0])
# words = open("/Users/alex.rosen/personal/xword/corpora/most-common-words.txt").readlines()
# for word in words:
#     entries.add(word.lower().rstrip())


animals = open("/Users/alex.rosen/personal/xword/corpora/animals.txt").read().splitlines()
numbers = ['one', 'two', 'three', 'four', 'five', 'six','seven','eight','nine','ten','eleven','twelve','thirteen','fourteen','fifteen','sixteen','seventeen','eighteen','twenty','thirty','forty','fifty','sixty','seventy','eighty','ninety','ahundred']

for entry in entries:
    for number in numbers:
        if entry.startswith(number):
            e2 = entry[len(number):]
            # print(entry, e2)
            for animal in animals:
                if e2.startswith(animal):
                    print(entry)