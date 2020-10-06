import sys

import puz, os
from puz_helpers import count_threes, is_open, all_entries, print_puzzle
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
          if k == '-' and length >= 7:
              themers.append(length)
    # for x in range(1, p.width-1):
    #     for y in range(1, p.height-1):
    #         if not is_open(p, [x-1, y]) and not is_open(p, [x, y-1]) and not is_open(p, [x+1, y+1])\
    #                 and is_open(p, [x-1, y-1]) and is_open(p, [x, y+1])and is_open(p, [x+1, y])\
    #                 and is_open(p, [x+1, y-1])and is_open(p, [x-1, y+1]):
    #             print(f)
    return (themers, p)

def stats(p):
    by_length = Counter()
    numbering = p.clue_numbering()
    for clue in numbering.across:
        by_length[clue['len']] += 1
    for clue in numbering.down:
        by_length[clue['len']] += 1
    return by_length

def find_puzzles():
    rootDir = '/Users/alex.rosen/personal/xword/nyt-archive'
    counter15 = Counter()
    counter21 = Counter()
    for dirName, subdirList, fileList in os.walk(rootDir):
        # print('Found directory: %s' % dirName)
        for fname in fileList:
            seven_plus, p = load(dirName + '/' + fname)
            threes = stats(p)[3]
            if p.width == 15 and p.height == 15:
                counter15[threes] += 1
            if p.width == 21 and p.height == 21:
                counter21[threes] += 1

    print("15x15")
    for n in range(8, 30, 2):
        print(n, int(counter15[n]/counter15.)
    print()
    print("21x21")
    for n in range(10, 40, 2):
        print(n, counter21[n])

find_puzzles()