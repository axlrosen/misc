import os, re
from collections import Counter
from time import sleep

import requests

import puz
from puz import load
from puz_helpers import all_entries

def process(path):
    lines = []
    with open(path, "r") as f:
        for line in f:
            word, score = line.rstrip().split(';')
            score = int(score)
            if score <= 20:
                score = 0
            elif score <= 25:
                score = 5
            elif score == 26:
                score = 20
            else:
                score *= 2
            lines.append(word + ";" + str(score))

    with open(path, "w", buffering=1) as out:
        for line in lines:
            print(line, file=out)


# with os.scandir('/Users/alex.rosen/personal/xword/dicts/') as it:
#     for entry in it:
#         if entry.name.endswith(".dict"):
#             process(entry.path)

process('/Users/alex.rosen/MyEdits.dict')