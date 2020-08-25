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
words = open("/Users/alex.rosen/personal/xword/corpora/most-common-words.txt").readlines()
words = {word.lower().rstrip() for word in words}
for entry in entries:
    words.add(entry)
# for word in words:
#     entries.add(word.lower().rstrip())

def find(inword, outword):
    found = set()
    for entry in entries:
        if len(entry) < 9: continue
        for i in range(2, len(entry)-1):
            left = entry[:i]
            right = entry[i:]
            if (left + inword in entries and outword + right in entries
                # and (left not in words or right not in words)
                and left not in {}
                and right not in {"ings", "ed", "er", "in", "ly"}
                and left not in {outword}
                and right not in {inword}
                and (left not in words or right not in words)
                and (len(left) == 2 or len(right) == 2)
                and outword+right not in ( "erles", "insts")
            ):
                x = (left+right+" "+ left+ inword + " "+outword +right)
                found.add(x)
    if len(found) > 0:
        print(inword+"and"+outword, "-", ", ".join(found))

pronoun_entries = {"youandme", "youandi", "usandthem", "heandshe", "sheandhe", "himandher", "hisandhers", "themandyou", "themandi",
                    "meandyou", "themandus", "youandhe", "youandshe", "sheandyou", "heandyou"}

find("ampers", "")

for entry in sorted(list(entries)):
    # if len(entry) > 7: continue
    if len(entry) < 8: continue
    if "and" in entry:
        pair = entry.split("and")
        inword = pair[0]
        outword = pair[1]
        # print(inword, outword)
        if len(inword) >= 1 and len(outword) >= 1:  # and inword[0] in "aeiouy" and outword[-1] in "aeiouy":
            find(inword, outword)
