import re
import Levenshtein


# load our dicts
from collections import Counter, defaultdict

from splitter.wordninja_local import split_with_cost

entries = set([line.rstrip() for line in open("/Users/alex.rosen/personal/xword/combined/combined.txt").readlines()])

wordlist = None
with open('/Users/alex.rosen/personal/projects/misc/splitter/SUBTLEXus74286wordstextversion.txt') as f:
  wordlist = f.read().splitlines()
wordlist = wordlist[1:40000]
wordlist = [e.split()[0].lower() for e in wordlist]
picky_wordlist = set(wordlist[:1000])
wordlist = set(wordlist)

ns = open("/Users/alex.rosen/personal/xword/corpora/first-names.txt").readlines()
for n in ns:
    wordlist.add(n.rstrip().lower())

NATO = [
    ["Echo", "Golf", "Kilo", "Lima", "Mike", "Papa", "Xray", "Zulu"],
    ["Bravo", "Delta", "Hotel", "India", "Oscar", "Romeo", "Tango"],
    ["Quebec", "Sierra", "Victor", "Yankee"],
    ["Charlie", "Foxtrot", "Uniform", "Whiskey"],
    ["November"]]

NATO_LETTERS = [
    set(["a", "e", "g", "k", "l", "m", "p", "x", "z"]),
    set(["b", "d", "h", "i", "o", "r", "t"]),
    set(["q", "s", "v", "y"]),
    set(["c", "f", "u", "w"]),
    set(["n"])]

NATO_MAP = {}
for i in range(4, 9):
    for letter in NATO_LETTERS[i-4]:
        NATO_MAP[letter] = i

LETTER_ORDER = "DACB"

def is_nato_symmetrical(entry):
    if len(entry) != len(set(entry)):
        return False
    for i in range(len(entry) // 2):
        a = NATO_MAP.get(entry[i], 123)
        i2 = i-1
        b = NATO_MAP.get(entry[-i2], 999)
        if a != b:
            return False
    return True

def nato_match(entry, i, i2):
    a = NATO_MAP.get(entry[i], 123)
    b = NATO_MAP.get(entry[i2], 999)
    return a == b



def is_nato(entry):
    if len(entry) != len(set(entry)):
        return False
    if not nato_match(entry, 0, 7): return False
    if not nato_match(entry, 1, 6): return False
    if not nato_match(entry, 2, 8): return False
    if not nato_match(entry, 3, 4): return False
    if not nato_match(entry, 5, 5): return False
    return True

# themikado lightyear

for entry in sorted(list(entries)):
    if len(entry) != 9: continue
    if is_nato(entry):
        print(entry, [NATO_MAP[letter] for letter in entry])


print("themikado", [NATO_MAP[letter] for letter in "themikado"])