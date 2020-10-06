import re
import sys

from nltk.corpus import brown
import nltk

NONASCII = re.compile("[^a-z]")

def clean(w):
    return NONASCII.sub('', w.lower())

def t():
    fd = nltk.FreqDist(clean(word) for word in brown.words())
    cfd = nltk.ConditionalFreqDist((clean(word), pos) for (word, pos) in brown.tagged_words(tagset='universal'))
    fd.pop("")
    # for pos in list(cfd["well"]):
    #     print(pos, cfd["well"][pos], cfd["well"].freq(pos))
    # print(cfd["well"].N())
    most_freq_words = fd.most_common(100000)
    for word, freq in most_freq_words:
        print(word, " ".join(pos for pos in cfd[word] if cfd[word].freq(pos) > .01))

t()