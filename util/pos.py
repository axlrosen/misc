from collections import Counter, defaultdict
from random import randrange
from statistics import mean

import nltk
from nltk.corpus import brown
import pickle
from splitter.wordninja_local import split, strict_phrase, loose_phrase, phrase

FILENAME = "/Users/alex.rosen/personal/xword/combined/phrase_classifier.pickle"

def write_pickle():
    word_freqs = nltk.FreqDist([w.lower() for w in brown.words()]).most_common()
    words_by_freq = [w for (w, _) in word_freqs]
    cfd = nltk.ConditionalFreqDist([(a.lower(), b) for a, b in brown.tagged_words(tagset='universal')])
    lt = dict((word, cfd[word].max()) for word in words_by_freq)
    baseline_tagger = nltk.UnigramTagger(model=lt, backoff=nltk.DefaultTagger('UNK'))
    # print(baseline_tagger.tag("Let's briefly return to the kinds of exploration of corpora we saw in previous chapters.".split()))

    # entries = open("/Users/alex.rosen/personal/xword/combined/combined.txt").readlines()
    entries = open("/Users/alex.rosen/personal/xword/dicts/broda-list-03.2020-trimmed-by-diehl.dict").readlines()
    entries = [word.split(';')[0] for word in entries]

    counts = defaultdict(Counter)
    totals = Counter()
    for entry in entries:
        tags = baseline_tagger.tag(split(entry))
        tags = [x[1] for x in tags]
        if 'UNK' in tags:
            # print(split(entry), tags)
            continue
        counts[len(tags)][tuple(tags)] += 1
        totals[len(tags)] += 1

    pickle.dump((baseline_tagger, counts, totals), open( FILENAME, "wb" ) )

baseline_tagger, counts, totals = pickle.load( open( FILENAME, "rb" ) )

def is_phrase(s, threshhold = .001):
    if type(s) == str:
        s = split(s)
    if any(len(word) == 1 and not word in "ai" for word in s): return None
    tags = baseline_tagger.tag(s)
    tags = [x[1] for x in tags]
    if 'UNK' in tags: return None
    count = counts[len(tags)].get(tuple(tags), 0)
    total = totals[len(tags)]
    ratio = count / total if total else 0
    # print(split(s), tags, freq, totals[len(tags)], ratio)
    return ratio > threshhold

def combo(s):
    return loose_phrase(s) or is_phrase(s)

def scramble(s):
    if len(s) < 2: return s
    i = randrange(len(s))
    j = randrange(len(s)-1)
    if j >= i:
        j += 1
    else:
        i, j = j, i
    return s[:i] + s[j] + s[i+1:j] + s[i] + s[j+1:]

def test_one(entries, bad_entries, func, desc):
    good = mean(1 if func(w) else 0 for w in entries)
    bad = mean(1 if not func(w) else 0 for w in bad_entries)
    print(f"{desc:12} {good*100:.1f}   {bad*100:.1f}")

def test():
    combined = open("/Users/alex.rosen/personal/xword/combined/combined.txt").readlines()
    entries = [word.rstrip() for word in combined][::10]
    entries = [w for w in entries if w]
    bad_entries = [scramble(w) for w in entries]
    test_one(entries, bad_entries, lambda x: loose_phrase(x) or is_phrase(x), "combo1")
    test_one(entries, bad_entries, lambda x: phrase(x) or is_phrase(x), "combo2")
    test_one(entries, bad_entries, lambda x: strict_phrase(x) or is_phrase(x), "combo3")
    test_one(entries, bad_entries, lambda x: is_phrase(x, .05), ".05")
    test_one(entries, bad_entries, lambda x: is_phrase(x, .02), ".02")
    test_one(entries, bad_entries, lambda x: is_phrase(x, .01), ".01")
    test_one(entries, bad_entries, lambda x: is_phrase(x, .005), ".005")
    test_one(entries, bad_entries, lambda x: is_phrase(x, .001), ".001")
    test_one(entries, bad_entries, lambda x: is_phrase(x, 0), "0")
    test_one(entries, bad_entries, loose_phrase, "loose_phrase")
    test_one(entries, bad_entries, phrase, "phrase")
    test_one(entries, bad_entries, strict_phrase, "strict_phrase")

# write_pickle()
# test()