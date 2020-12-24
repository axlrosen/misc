import re
from typing import List, Set

import Levenshtein
import unidecode

from splitter.wordninja_local import split
from util.pos import is_phrase

NONLETTERS = re.compile("[^a-z]")

# combined = open("/Users/alex.rosen/personal/xword/corpora/FamousNames.txt").readlines()
# entries = [word.rstrip().split("\t") for word in combined]
# entries = [word[0].lower() for word in entries if int(word[1]) >= 95]
# entries = [unidecode.unidecode(e) for e in entries]
# entries = [NONLETTERS.sub("", e) for e in entries]

xwordinfo_words = open("/Users/alex.rosen/personal/xword/combined/combined15.txt").readlines()
entries = [word.rstrip().lower() for word in xwordinfo_words]

NOTES = ['do', 're', 'mi', 'fa', 'sol', 'la', 'ti']
# NOTES = ['nw', 'ne', 'sw', 'se']
# OPPOSITES = {'nw':'se', 'ne':'sw', 'sw':'ne', 'se':'nw'}

def get_transformed(e: str, result: Set[str]):
    if not "[" in e:
        result.add(e)
        return

    for note in NOTES:
        if "[" + note.upper() + "]" in e:
            # e2 = e.replace("[" + note.upper() + "]", OPPOSITES[note])
            # get_transformed(e2, result)

            for note2 in NOTES:
                if note == note2: continue
                e2 = e.replace("[" + note.upper() + "]", note2)
                get_transformed(e2, result)

for e in sorted(entries):
    if len(e) < 11: continue
    if len(e) > 16: continue
    count = 0
    e2 = e
    for note in NOTES:
        while note in e2:
            e2 = e2.replace(note, "[" + note.upper() + "]")
            count += 1
    if count >= 2:
        transformed = set()
        get_transformed(e2, transformed)
        for t in transformed:
            if is_phrase(t, 0):
                sp = split(t)
                is_good = True
                for note in NOTES:
                    if note in sp:
                        is_good = False
                if is_good and not set(split(e)).intersection(set(sp)) and len(sp) <= 3:
                    print(e, " ".join(sp))
    if count == 1:
        sp1 = split(e)
        transformed = set()
        get_transformed(e2, transformed)
        for t in transformed:
            if is_phrase(t, 0):
                sp = split(t)
                is_good = True
                for note in NOTES:
                    if note in sp:
                        is_good = False
                if is_good and not set(sp1).intersection(set(sp)) and len(sp) <= 3:
                    print(e, " ".join(sp))



