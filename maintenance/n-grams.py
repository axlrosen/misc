import sys
from collections import Counter

with open(sys.argv[1], "r") as f:
    prev = None
    prev2 = None
    twograms = Counter()
    linecount = 0
    for line in f:
        words = line.lower().split()
        for word in words:
            if prev and prev2:
                twogram = prev + " " + prev2 + " " + word
                twograms[twogram] += 1
            prev = prev2
            prev2 = word
        linecount += 1
        if linecount % 100000 == 0:
            print(linecount)

    for k, v in twograms.items():
        if v >= 2:
            print(k, v)

