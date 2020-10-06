from datetime import datetime

import puz, os
from puz_helpers import count_threes, is_open, is_rotational, print_puzzle, across_length
from itertools import groupby
from collections import defaultdict, Counter

def load(f):
    p = puz.read(f)
    themers = []
    for row_num in range(p.height):
      cell = row_num * p.width
      row = p.fill[cell:cell + p.width]
      for k,g in groupby(row):
          length = len(list(g)) 
          if k == '-' and length >= 8:
              themers.append(length)
    return (themers, p)

def count_theme_lengths():
    root_dir = '/Users/alex.rosen/personal/xword/nyt-archive'
    counter = Counter()
    puzzles = defaultdict(list)
    for dirName, subdirList, fileList in os.walk(root_dir):
        if not "nyt-archive/20" in dirName:
            continue
        print('Found directory: %s' % dirName)
        for fname in fileList:
            date_string = fname[:3] + " " + fname[3:5] + " 20" + fname [5:7]
            date = datetime.strptime(date_string, "%b %d %Y")
            if date.weekday() in [0, 1, 2]:
                themers, p = load(dirName + '/' + fname)
                key = tuple(sorted(themers, reverse=True))
                counter[key] += 1
                puzzles[key].append(date)

    for themers, count in counter.most_common():
        s = ""
        for length in themers:
            s += format(length, "X")
        puzzles[themers].sort(reverse=True)
        dates = [date.strftime("%b %d %Y") for date in puzzles[themers][:4]]
        dates = ", ".join(dates)
        print(f"{s}  {count}     ({dates})")

def count_middles():
    root_dir = '/Users/alex.rosen/personal/xword/nyt-archive'
    counter = Counter()
    puzzles = defaultdict(list)
    for dirName, subdirList, fileList in os.walk(root_dir):
        if not "nyt-archive/201" in dirName:
            continue
        print('Found directory: %s' % dirName)
        for fname in fileList:
            date_string = fname[:3] + " " + fname[3:5] + " 20" + fname [5:7]
            date = datetime.strptime(date_string, "%b %d %Y")
            if date.weekday() in [0, 1, 2]:
                themers, p = load(dirName + '/' + fname)
                if is_rotational(p) and p.width == 15 and p.height == 15 and is_open(p, [7,7]):
                    for x in range(7, -1, -1):
                        xlen = across_length(p, [x, 7])
                        if xlen:
                            counter[xlen] += 1
                            break
    for len in range(0, 16):
        print(len, counter[len])

count_middles()
