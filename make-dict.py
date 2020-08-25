import re
import sys

import Levenshtein


# load our dicts
from collections import Counter, defaultdict

entries = {}
DICTS = ["broda-list-03.2020-trimmed-by-diehl.dict", "XwiWordList_delta_June2020.dict", "CLUED.dict", "XwiWordList_updated3456.dict",
         "my-bonuses.dict", "my-good-words.dict", "../../../MyEdits.dict"]
with open("/Users/alex.rosen/personal/xword/dicts/sparklingfill.txt", "w") as out:
    for dictfile in reversed(DICTS):
        broda = open("/Users/alex.rosen/personal/xword/dicts/" + dictfile).readlines()
        precount = len(entries)
        for word in broda:
            parts = word.lower().split(';')
            if parts[0] not in entries:
                if len(parts) == 1:
                    print("XXX", word)
                    sys.exit(1)
                entries[parts[0]] = parts[1]
                out.write(f"{parts[0]},{parts[1]}")
        print(dictfile, len(entries) - precount)


