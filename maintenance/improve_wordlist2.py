import os, re
from collections import Counter
from time import sleep

import requests

import puz
from puz import load
from puz_helpers import all_entries

def count_words():
    words = []
    root_dir = '/Users/alex.rosen/personal/xword/nyt-archive'
    counter = Counter()
    for dirName, subdirList, fileList in os.walk(root_dir):
        # print('Found directory: %s' % dirName)
        for fname in fileList:
            p = puz.read(dirName + '/' + fname)
            for entry in all_entries(p):
                entry = entry.lower()
                counter[entry] += 1
                if counter[entry] == 3:
                    words.append(entry)
    return words

nytimes_words = count_words()

word_list = '/Users/alex.rosen/personal/xword/dicts/XwiWordList_updated3456.dict'
word_list_out = '/Users/alex.rosen/personal/xword/dicts/XwiWordList_autodemoted50to473727_autodemoted25to20.dict'
n = 0
with open(word_list, "r") as f, open(word_list_out, "a", buffering=1) as out:
    for line in f:
        word, score = line.rstrip().split(';')
        if score == '25':
            word = word.lower()
            if word not in nytimes_words:
                score = "20"
        print(word + ";" + score, file=out)
