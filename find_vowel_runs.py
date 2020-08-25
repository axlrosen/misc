import re

# load our dicts
from collections import Counter, defaultdict

entries = set()
clued_words = open("/Users/alex.rosen/personal/xword/dicts/CLUED.dict").readlines()
for word in clued_words:
    entries.add(word.split(';')[0].lower())
xwordinfo_words = open("/Users/alex.rosen/personal/xword/dicts/XwiWordList.dict").readlines()
for word in xwordinfo_words:
    entries.add(word.split(';')[0])

has_two_vowels = re.compile("[aeiou]..*[aeiou]")
vowel_pattern = re.compile("[aeiou]")

word_sets = defaultdict(set)
def check(word):
    vowelless = vowel_pattern.sub("", word)
    word_sets[vowelless].add(word)

for word in entries:
    if len(word) > 8 and has_two_vowels.search(word):
        check(word)

counts = Counter()
for word_set in word_sets.values():
    counts[frozenset(word_set)] = sum(len(w) for w in word_set)

print(counts.most_common(20))
