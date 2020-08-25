from datetime import datetime

import puz, os
from puz_helpers import count_threes, is_open
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

def find_puzzles():
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

find_puzzles()
