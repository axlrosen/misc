import re
from collections import defaultdict

pattern = re.compile("[^A-Z ]")
prons = defaultdict(set)

def guess_pron(word):
    if word in prons:
        return prons[word]
    guesses = set()
    length = len(word)
    for i in range(length):
        left = word[:i]
        right = word[i:]
        if left in prons and right in prons:
            for left_pron, right_pron in zip(prons[left], prons[right]):
                guess = left_pron + " " + right_pron
                guesses.add(guess)

    return guesses

def load_dict():
    with open('/Users/alex.rosen/personal/xword/dicts/cmudict-0.7b', "r", encoding='latin1') as f:
        for line in f:
            if line.startswith(';'):
                continue
            line = pattern.sub('', line)
            word, pron = line.split('  ')
            prons[word.lower()].add(pron)

def guess_prons():
    with open('/Users/alex.rosen/personal/xword/dicts/XwiWordList_updated3456.dict', "r") as f:
        for line in f:
            word, score = line.rstrip().split(';')
            prons = guess_pron(word)
            for pron in prons:
                print(f"{pron}/{word};{score}")

load_dict()
guess_prons()
