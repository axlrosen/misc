import gzip, os, re
from math import log


__version__ = '2.0.0'


# I did not author this code, only tweaked it from:
# http://stackoverflow.com/a/11642687/2449774
# Thanks Generic Human!


# Modifications by Scott Randal (Genesys)
#
# 1. Preserve original character case after splitting
# 2. Avoid splitting every post-digit character in a mixed string (e.g. 'win32intel')
# 3. Avoid splitting digit sequences
# 4. Handle input containing apostrophes (for possessives and contractions)
#
# Wordlist changes:
# Change 2 required adding single digits to the wordlist
# Change 4 required the following wordlist additions:
#   's
#   '
#   <list of contractions>


class LanguageModel(object):
  def __init__(self):
    # Build a cost dictionary, assuming Zipf's law and cost = -math.log(probability).
    with gzip.open('/Users/alex.rosen/personal/projects/misc/splitter/wordninja_words.txt.gz') as f:
      words = f.read().decode().split()
    with open('/Users/alex.rosen/personal/projects/misc/splitter/wordninja_supplement.txt') as f:
      words.extend(f.read().splitlines())
    self._wordcost = dict((k, log((i+1)*log(len(words)))) for i,k in enumerate(words))
    self._maxword = max(len(x) for x in words)
   
  def xxx__init__(self):
    # main dict
    with open('/Users/alex.rosen/personal/projects/misc/splitter/SUBTLEXus74286wordstextversion.txt') as f:
      wordlines = f.read().splitlines()
    wordlines = wordlines[1:]
    self._wordcost = {}
    for line in wordlines:
      parts = line.split()
      self._wordcost[parts[0]] = 7 - float(parts[6])
    self._maxword = max(len(x) for x in self._wordcost.keys())

    # backstop dict
    with gzip.open('/Users/alex.rosen/personal/projects/misc/splitter/wordninja_words.txt.gz') as f:
      words = f.read().decode().split()
    for w in words:
      if not w in self._wordcost:
        self._wordcost[w] = 7
    self._maxword = 7

    # backstop dict
    peter_words = open("/Users/alex.rosen/personal/xword/dicts/broda-list-03.2020-trimmed-by-diehl.dict").readlines()
    for w in peter_words:
      w = w.split(';')[0].lower()
      if not w in self._wordcost:
        self._wordcost[w] = 7

  def split(self, s):
    """Uses dynamic programming to infer the location of spaces in a string without spaces."""
    l = [self._split(x) for x in _SPLIT_RE.split(s)]
    return [item for sublist in l for item in sublist]


  def _split(self, s):
    # Find the best match for the i first characters, assuming cost has
    # been built for the i-1 first characters.
    # Returns a pair (match_cost, match_length).
    def best_match(i):
      candidates = enumerate(reversed(cost[max(0, i-self._maxword):i]))
      return min((c + self._wordcost.get(s[i-k-1:i].lower(), 9e999), k+1) for k,c in candidates)

    # Build the cost array.
    cost = [0]
    for i in range(1,len(s)+1):
      c,k = best_match(i)
      cost.append(c)

    # Backtrack to recover the minimal-cost string.
    out = []
    i = len(s)
    total_cost = 0
    while i>0:
      c,k = best_match(i)
      assert c == cost[i]
      # Apostrophe and digit handling (added by Genesys)
      new_token = True
      if not s[i-k:i] == "'": # ignore a lone apostrophe
        if len(out) > 0:
          # re-attach split 's and split digits
          if out[-1] == "'s" or (s[i-1].isdigit() and out[-1][0].isdigit()): # digit followed by digit
            out[-1] = s[i-k:i] + out[-1] # combine current token with previous token
            new_token = False
      # (End of Genesys addition)

      if new_token:
        out.append(s[i-k:i])
        total_cost += c

      i -= k

    return reversed(out), total_cost

DEFAULT_LANGUAGE_MODEL = LanguageModel()
_SPLIT_RE = re.compile("[^a-zA-Z0-9']+")

def split(s):
  return list(DEFAULT_LANGUAGE_MODEL.split(s)[0])

def split_with_cost(s):
  return DEFAULT_LANGUAGE_MODEL.split(s)

def phrase(s):
  phrase, cost = split_with_cost(s)
  phrase = list(phrase)
  if cost / len(phrase)**1.5 > 10: return False
  for index, word in enumerate(phrase):
    if len(word) == 1 and (word != "i" or index != 0) and word != "a": return False
  return phrase, cost

def strict_phrase(s):
  phrase, cost = split_with_cost(s)
  phrase = list(phrase)
  if cost / len(phrase)**1.5 > 9: return False
  for index, word in enumerate(phrase):
    if len(word) == 1: return False
  return phrase, cost

def loose_phrase(s):
  phrase, cost = split_with_cost(s)
  phrase = list(phrase)
  if cost / len(phrase)**1.5 > 11.5: return False
  for index, word in enumerate(phrase):
    if len(word) == 1 and (word != "i" or index != 0) and word != "a": return False
  return phrase, cost

#
# GOOD=["try", "chess","ugly","itsugly","itry","foryouitsok","amaninfull", "treesfallin", "whatisgoingonhere","theresnocryingin","woulditbenicetodo"]
# BAD=["tyr","cshess","llgy","istulyg","irty","foryositok","ananifull","treselfalin","awefawefawefawef","abababababababa","aaaaaaaaaaaaaaa"]
#
# for w in GOOD:
#   sp, cost = split(w)
#   print(f"{cost / len(w)**1.5:.1f} ", end="")
# print()
# for w in BAD:
#   sp, cost = split(w)
#   print(f"{cost / len(w)**1.5:.1f} ", end="")
#
# print()
# for w in GOOD:
#   sp, cost = split(w)
#   print(f"{cost / len(list(sp))**1.5:.1f} ", end="")
# print()
# for w in BAD:
#   sp, cost = split(w)
#   print(f"{cost / len(list(sp))**1.5:.1f} ", end="")