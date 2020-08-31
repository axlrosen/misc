import splitter.wordninja_local
import wordninja
import re
from collections import defaultdict

# load our dicts
entries = set()
clued_words = open("/Users/alex.rosen/personal/xword/dicts/CLUED.dict").readlines()
for word in clued_words:
    entries.add(word.split(';')[0].lower())
# peter_words = open("/Users/alex.rosen/personal/xword/dicts/broda-list-03.2020-trimmed-by-diehl.dict").readlines()
# for word in peter_words:
#     entries.add(word.split(';')[0].lower())
xwordinfo_words = open("/Users/alex.rosen/personal/xword/dicts/XwiWordList_upgraded25s.dict").readlines()
for word in xwordinfo_words:
    entries.add(word.split(';')[0])
xwordinfo_words = open("/Users/alex.rosen/personal/xword/dicts/XwiWordList_delta_June2020.dict").readlines()
for word in xwordinfo_words:
    entries.add(word.split(';')[0])

# load pron dict
pattern = re.compile("[^A-Z ]")
pron_dict = {}
with open('/Users/alex.rosen/personal/xword/corpora/cmudict-0.7b', "r", encoding='latin1') as f:
    for line in f:
        if line.startswith(';'):
            continue
        line = pattern.sub('', line)
        word, pron = line.split('  ')
        if not word.lower() in pron_dict:
            pron_dict[word.lower()] = pron.replace(' ', '-')

entries = sorted(list(entries))

def guess_pron(words):
    prons = []
    for word in words:
        if not word in pron_dict:
            return []
        prons.append(pron_dict[word])
    return prons

out = []
count = 0
for entry in entries:
    words = wordninja.split(entry)
    # words_bad = splitter.wordninja_local.split(entry)
    # prons = guess_pron(words)
    # out.append(entry + "/" + " ".join(words) + "/" + " ".join(prons) + "\n")
    if len(entry) <= 15:
        out.append(" ".join(words) + "\n")
    # count += 1
    # if count % 5001 == 0:
    #     print(entry," ".join(words) )

open("/Users/alex.rosen/personal/xword/combined/split15.txt", "w").writelines(out)
