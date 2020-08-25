import sys

import puz, os
from puz_helpers import count_threes, is_open, all_entries
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
    return (themers, p)

def stats(p):
    by_length = Counter()
    numbering = p.clue_numbering()
    for clue in numbering.across:
        by_length[clue['len']] += 1
    for clue in numbering.down:
        by_length[clue['len']] += 1
    return by_length

def find_puzzles(condition):
    rootDir = '/Users/alex.rosen/personal/xword/nyt-archive'
    counter = Counter()
    puzzles = defaultdict(set)
    for dirName, subdirList, fileList in os.walk(rootDir):
        # print('Found directory: %s' % dirName)
        for fname in fileList:
            seven_plus, p = load(dirName + '/' + fname)
            if condition(seven_plus, p):
                counter[p.fill] += 1
                puzzles[p.fill].add((p, fname))
    for fill, count in counter.most_common():
        fnames = set(fname for (p, fname) in puzzles[fill])
        p, fname = puzzles[fill].pop()
        print_puzzle(seven_plus, p, fnames, count)


def print_puzzle(themers, p, filenames, count):
    print(f"{count} {filenames}  {len(p.clues)} words, {count_threes(p)} threes")
    for row in range(p.height):
        cell = row * p.width
        print(p.fill[cell:cell + p.width].replace('.', '\u2588').replace('-', '.'), "     ", p.solution[cell:cell + p.width])
    print

def is_good(p):
    by_length = stats(p)
    if by_length[3] > 20:
        return False
    if len(p.clues) != 78:
        return False
    total_long = 0
    for len2 in range(8, 15):
        for i in range(by_length[len2]):
            total_long += len2
    return total_long < 70

def matches_themers(seven_plus, desired_themers, ordered):
    m = min(desired_themers)
    themers = [length for length in seven_plus if length >= m]
    if not ordered:
        themers.sort()
        desired_themers.sort()
    return themers == desired_themers

def is_jungle_gym(p):
    for x in range(1, 20, 2):
        if not is_open(p, [x, 6]): return False
    for y in range(8, 19, 2):
        if not is_open(p, [0, y]): return False
        if not is_open(p, [20, y]): return False
    # if is_open(p, [4, 6]) or is_open(p, [8, 6]) or is_open(p, [12, 6]) or is_open([p, 16, 6]): return False
    return True

desired_themers = [12, 12, 11, 11, 8, 8]
ordered = False
find_puzzles(lambda seven_plus, p:
             p.width < 20 and p.height < 20 and
             matches_themers(seven_plus, desired_themers, ordered) and
             is_good(p))

# find_puzzles(lambda themers, p: p.width == 15 and p.height == 15 and p.fill[10*15+10] == '.' and p.fill[12*15+8] == '.' and is_good(p))
# find_puzzles(lambda themers, p: p.width == 21 and p.height == 21 and is_jungle_gym(p))
