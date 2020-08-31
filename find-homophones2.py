import gzip

import Levenshtein


def to_pron(pron: str):
    return pron.replace('0', '').replace('1', '').replace('2', '')

def check(pron, w, entries, prefix):
    if prefix + pron in entries:
        w2 = entries[prefix + pron]
        dist = Levenshtein.distance(w, w2)
        if dist > 2:
            print(w, w2, pron)

entries = {}
f = open("/Users/alex.rosen/personal/xword/corpora/cmudict-0.7b-dots2.txt", encoding="latin-1")
for line in f:
    words = line.split()
    entries[to_pron(words[1])] = words[0]

for pron, w in entries.items():
    check(pron, w, entries, "AH.")
    check(pron, w, entries, "AE.")
    check(pron, w, entries, "AA.")

