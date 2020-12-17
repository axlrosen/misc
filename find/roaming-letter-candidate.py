import re
import sys

import Levenshtein
from collections import Counter, defaultdict
import nltk
import wordninja

from splitter.wordninja_local import split
from util.pos import is_phrase

combined = open("/Users/alex.rosen/personal/xword/combined/combined15.txt").readlines()
entries = set([word.rstrip() for word in combined])

with open('/Users/alex.rosen/personal/projects/misc/splitter/SUBTLEXus74286wordstextversion.txt') as f:
  wordlist = f.read().splitlines()
wordlist = wordlist[1:10000]
wordlist = set([e.split()[0].lower() for e in wordlist])


LETTER = "i"

donors = set()
donees = set()
both = {}

ROMANS = set("ivxlcdm")
def is_roman(s):
    return len(set(s).difference(ROMANS)) == 0

for entry in sorted(list(wordlist)):
    i = entry.find(LETTER)
    if len(entry) >= 4 and i >= 0:
        transformed = entry[:i] + entry[i+1:]
        if not LETTER in transformed and transformed in wordlist:
            if not is_roman(entry):
                donors.add(entry)
                donees.add(transformed)
                both[entry] = transformed
                # print(entry, transformed)


for entry in sorted(list(entries)):
    if len(entry) < 14: continue
    for donor, donee in both.items():
        if donee in entry:
            i = entry.find(LETTER)
            if i >= 0 and entry.find(LETTER, i+1) == -1:
                if i == 0 or i == len(entry)-1 or entry[i-1] in "aeiouy" or entry[i+1] in "aeiouy":
                    shrunk = entry[:i] + entry[i + 1:]
                    transformed = shrunk.replace(donee, donor)
                    sp = split(transformed)
                    if len(sp) <= 4 and not is_phrase(transformed, 0):
                        print(" ".join(split(entry)), "/", " ".join(split(transformed)))

#
# for entry in sorted(list(entries)):
#     if len(entry) < 14: continue
#     for donor, donee in both.items():
#         if donor in entry:
#             i = entry.find(donor)
#             shrunk = entry[:i] + entry[i + len(donor):]
#             if not LETTER in shrunk:
#                 for donor2, donee2 in both.items():
#                     if donee2 in shrunk and donee2 in entry and not donor2 in shrunk and donor2 != donor:
#                         i = shrunk.find(donee2)
#                         if i >= 0:
#                             transformed = entry.replace(donor, donee).replace(donee2, donor2)
#                             sp = split(transformed)
#                             if len(sp) <= 3:
#                                 print(" ".join(split(transformed)), "/", donor, donor2)
