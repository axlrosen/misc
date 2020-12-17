# IIRC my splitter is worse than the ninja one

import gzip, os, re
import sys
from math import log

# load our dicts
entries = set()
clued_words = open("/Users/alex.rosen/personal/xword/dicts/CLUED.dict").readlines()
for word in clued_words:
    entries.add(word.split(';')[0].lower())
peter_words = open("/Users/alex.rosen/personal/xword/dicts/broda-list-03.2020-trimmed-by-diehl.dict").readlines()
for word in peter_words:
    entries.add(word.split(';')[0].lower())
xwordinfo_words = open("/Users/alex.rosen/personal/xword/dicts/XwiWordList_updated3456.dict").readlines()
for word in xwordinfo_words:
    entries.add(word.split(';')[0])
xwordinfo_words = open("/Users/alex.rosen/personal/xword/dicts/XwiWordList_delta_June2020.dict").readlines()
for word in xwordinfo_words:
    entries.add(word.split(';')[0])

IGNORES = ["", "s", "es", "ed", "d", "er", "r", "ers", "ing", "ly", "a", "ings", ""]

class LanguageModel(object):
    def xxx__init__(self):
        # Build a cost dictionary, assuming Zipf's law and cost = -math.log(probability).
        with gzip.open('/Users/alex.rosen/personal/projects/misc/splitter/wordninja_words.txt.gz') as f:
            words = f.read().decode().split()
        self._wordcost = dict((k, log(( i +1 ) *log(len(words)))) for i ,k in enumerate(words))
        # 2.46 - 14.2
        # print(min(score for (word, score) in self._wordcost.items()))
        # print(max(score for (word, score) in self._wordcost.items()))
        for ignore in IGNORES:
            self._wordcost[ignore] = 9e999
        self._maxword = max(len(x) for x in words)

    def __init__(self):
        with open('/Users/alex.rosen/personal/projects/misc/splitter/SUBTLEXus74286wordstextversion.txt') as f:
            wordlines = f.read().splitlines()
        wordlines = wordlines[1:]
        self._wordcost = {}
        for line in wordlines:
            parts = line.split()
            self._wordcost[parts[0]] = float(parts[6])
        # 2.46 - 14.2
        print(min(score for (word, score) in self._wordcost.items()))
        print(max(score for (word, score) in self._wordcost.items()))
        for ignore in IGNORES:
            self._wordcost[ignore] = 9e999
        self._maxword = max(len(x) for x in self._wordcost.keys())

    def _cost(self, s):
        c = self._wordcost.get(s, 9e999)
        if len(s) == 1: c += 5
        if len(s) == 2: c += 1
        return c


    def split(self, s):
        splits = []
        for i in range(len(s)):
            cost = self._cost(s[:i]) + self._cost(s[i:])
            if cost < 20: # 24
                splits.append(([s[:i], s[i:]]))
            for j in range(i+1, len(s)):
                cost2 = self._cost(s[:i]) + self._cost(s[i:j]) + self._cost(s[j:])
                # print(cost2, [s[:i], s[i:j], s[j:]])
                if cost2 < 30: # 40
                    splits.append(([s[:i], s[i:j], s[j:]]))
        return splits



DEFAULT_LANGUAGE_MODEL = LanguageModel()
_SPLIT_RE = re.compile("[^a-zA-Z0-9']+")


def split(s):
    return DEFAULT_LANGUAGE_MODEL.split(s)

# print(split("rateaten"))
# sys.exit(0)

animals = open("/Users/alex.rosen/personal/xword/corpora/animals.txt").read().splitlines()


spilt_entries = set()
for entry in sorted(list(entries)):
    if len(entry) < 11: continue
    splits = split(entry)
    # print(splits)
    for s in splits:
        s = tuple(s)
        if "thousand" in s or "hundred" in s or "and" in s or "or" in s: continue
        if len(s) != 3: continue
        if s in spilt_entries: continue
        r = tuple(reversed(s))
        if r in spilt_entries:
            print(r)
        spilt_entries.add(s)

    # if len(splits) > 1:
    #     if splits[0][0] == splits[1][0] + "s" or splits[1][0] == splits[0][0] + "s": continue
    #     for animal in animals:
    #         for words in splits:
    #             if words[0] == animal:
    #                 starters = [w for w in splits if w[0] == animal or w[0] == animal + "s"]
    #                 if starters != splits:
    #                     print(splits)

