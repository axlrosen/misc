import puz, os, sys
from puz_helpers import *
from itertools import groupby
from collections import defaultdict, Counter

paints = set(r.rstrip().upper() for r in open('/Users/alex.rosen/personal/xword/dicts/paint.txt').readlines())
tniaps = set(r.rstrip().upper() for r in open('/Users/alex.rosen/personal/xword/dicts/tniap.txt').readlines())

class NotFoundError(BaseException):
    pass

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

def flip(fill):
    return "".join(fill[i:i+15] for i in range(0, len(fill), 15))

def find_puzzles(condition):
    rootDir = '/Users/alex.rosen/personal/xword/nyt-archive'
    seen = set()
    for dirName, subdirList, fileList in os.walk(rootDir):
        # print('Found directory: %s' % dirName)
        for fname in fileList:
            themers, p = load(dirName + '/' + fname)
            if p.width != 15 or p.height != 15:
                continue
            if p.fill in seen:
                continue
            seen.add(p.fill)
            condition(sorted(themers), p, dirName + '/' + fname)
            p.fill = flip(p.fill)
            condition(sorted(themers), p, dirName + '/' + fname)


def print_puzzle(p, filename):
    print(filename)
    for row in range(p.height):
        cell = row * p.width
        print(p.fill[cell:cell + p.width].replace('.', '\u2588').replace('-', '.'))
        # print(p.fill[cell:cell + p.width].replace('.', '\u2588').replace('-', '.'), "     ", p.solution[cell:cell + p.width])
    print
    print(list(p.added))


def is_good(by_length):
    if by_length[3] > 20:
        return False
    total_long = 0
    for len in range(8, 15):
        for i in range(by_length[len]):
            total_long += len
    return total_long < 45

def find_fits_down(p, loc, down_len, entries):
    result = set()
    for entry in entries:
        if len(entry) == down_len and fits_down(p, loc, entry):
            result.add(entry)
    return result

def find_fits_across(p, loc, across_len):
    for entry in paints:
        if len(entry) == across_len and fits_across(p, loc, entry):
            p.fill_across(loc, entry)
            return True
    for entry in tniaps:
        if len(entry) == across_len and fits_across(p, loc, entry):
            p.fill_across(loc, entry)
            return True
    return False

def all_longer_acrosses_have_fits(p, left_loc, right_loc):
    for x in range(0, 8):
        for y in range(0, 14):
            l = across_length(p, [x, y])
            if l <= 7:
                continue
            if l > 13:
                return False # not required, just to make things easier
            if x == 0 and y + 1 >= left_loc[1] >= y - 1:
                return False
            if x > 0 and y + 1 >= right_loc[1] >= y - 1:
                return False
            if not find_fits_across(p, [x, y], l):
                return False
    return True


def find_fits(p, loc1, loc2, down_len, entries1, entries2, filename, left_loc, right_loc):
    for entry1 in entries1:
        if len(entry1) == down_len and fits_down(p, loc1, entry1):
            for entry2 in entries2:
                if len(entry2) == down_len and fits_down(p, loc2, entry2):
                    p.fill_down(loc1, entry1)
                    p.fill_down(loc2, entry2)
                    if all_longer_acrosses_have_fits(p, left_loc, right_loc) and len(p.added) == 4:
                        print_puzzle(p, filename)
                    p.reset()


def find_fits_paint(themers, p, filename):
    left_loc = find_left(p, 7)
    right_loc = find_right(p, 7)
    if not left_loc or not right_loc:
        return False
    fill_across(p, left_loc, "JACKSON")
    fill_across(p, right_loc, "POLLOCK")
    p.snapshot()
    d1_loc, d2_loc = find_longest_downs(p)
    down_len = down_length(p, d1_loc)
    if not d1_loc or not d2_loc or down_len < 9 or down_len > 13:
        return False
    find_fits(p, d1_loc, d2_loc, down_len, paints, tniaps, filename, left_loc, right_loc)
    find_fits(p, d1_loc, d2_loc, down_len, tniaps, paints, filename, left_loc, right_loc)
    return False

def main():
    desired_themers = sorted([10, 10, 7, 7  ])
    # find_puzzles(lambda themers, p: p.width == 15 and p.height == 15 and themers == desired_themers and is_good(stats(p)))
    find_puzzles(lambda themers, p, filename: find_fits_paint(themers, p, filename))

    # find_puzzles(lambda themers, p: p.width == 15 and p.height == 15 and p.fill[10*15+10] == '.' and p.fill[12*15+8] == '.' and is_good(stats(p)))


if __name__ == "__main__":
    main()
