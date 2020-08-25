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

has_two_vowels = re.compile("[aeiou].*[aeiou]")
has_three_consonants = re.compile("[^aeiou].*[^aeiou].*[^aeiou].*[^aeiou]")
vowel_pattern = re.compile("[aeiou]")

word_sets = defaultdict(set)
counts = Counter()
def check(word):
    vowelless = vowel_pattern.sub("", word)
    for prev in word_sets[vowelless]:
        dist = Levenshtein.distance(prev, word)
        # if dist >= 5 and len(word) + len(prev) <= 15:
        #     print(dist, prev, word)
        counts[vowelless] += dist
    word_sets[vowelless].add(word)

for word in entries:
    if len(word) >= 6 and has_two_vowels.search(word) and has_three_consonants.search(word):
        check(word)

for vowelless, count in counts.most_common(500):
    if not vowelless.endswith("s"):
        print(word_sets[vowelless])

for vowelless, count in counts.most_common(500):
    if vowelless.endswith("s"):
        print(word_sets[vowelless])
    print(word_sets[vowelless])
