import re
import Levenshtein
import unidecode

from splitter.wordninja_local import split

NONLETTERS = re.compile("[^a-z]")

combined = open("/Users/alex.rosen/personal/xword/corpora/wikipedia-4a.txt").readlines()
entries = [word.split()[0].replace("_", "").split("(")[0].lower() for word in combined]
entries = [unidecode.unidecode(e) for e in entries]
entries = [NONLETTERS.sub("", e) for e in entries]
with open("/Users/alex.rosen/personal/xword/corpora/wikipedia-4a-stripped.txt", "w") as out:
    for e in entries:
        if e:
            out.write(e + "\n")

