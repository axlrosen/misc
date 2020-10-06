import gzip
from collections import defaultdict

with gzip.open('/Users/alex.rosen/personal/projects/misc/splitter/wordninja_words.txt.gz') as f:
    freqs = f.read().decode().split()[:20000]


def to_pron(pron: str):
    return pron.replace('0', '').replace('1', '').replace('2', '')

entries = defaultdict(set)
f = open("/Users/alex.rosen/personal/xword/corpora/cmudict-0.7b-dots2.txt", encoding="latin-1")
for line in f:
    words = line.lower().split()
    if words[0] in freqs:
        entries[to_pron(words[1])].add(words[0])

for pron, w in entries.items():
    if len(w) > 1:
        print(w)
