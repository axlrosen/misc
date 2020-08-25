import re

def print_all_potential_entries(condition):
    with open('/Users/alex.rosen/personal/xword/corpora/bnc/just-words.txt') as f:
        seen = set()
        for line in f:
            words = line.split()
            for i in range(len(words)):
                potential_entries = enumerate_potential_entries(words, i)
                for pe in potential_entries:
                    if pe not in seen:
                        if condition(pe):
                            print(pe)
                        seen.add(pe)

def enumerate_potential_entries(words, i):
    pe = ""
    while i < len(words):
        pe += words[i]
        if len(pe) <= 11:
            yield pe
        i += 1


regex = re.compile('t.*n.*i.*a.*p')
print_all_potential_entries(lambda pe: regex.search(pe))