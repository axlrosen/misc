import re
import sys

from nltk.corpus import brown
import nltk
from nltk.corpus import wordnet as wn

NONASCII = re.compile("[^a-z]")

def clean(w):
    return NONASCII.sub('', w.lower())

def t():
    cfd = nltk.ConditionalFreqDist((clean(word), pos) for (word, pos) in brown.tagged_words(tagset='universal'))

    names = sorted([n.lower() for n in nltk.corpus.names.words()])
    for name in names:
        if cfd[name].freq("VERB") > 0.1 and any(".v." in s.name() for s in wn.synsets(name)):
            print(name)

t()