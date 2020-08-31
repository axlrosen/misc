import os, re
from collections import Counter
from time import sleep

import requests

corpus_words = Counter()
regex = re.compile('[^a-z]')
wordcount_regex = re.compile('\\b([0-9,one]*) Shortz Era entr')

def add(word):
    if len(word) <= 15:
        corpus_words[word] += 1

def process(fpath):
    w = x = y = z = ""
    with open(fpath, "r") as f:
        for line in f:
            line = line.lower()
            line = regex.sub(' ', line)
            for word in line.split():
                (w, x, y, z) = (x, y, z, word)
                add(word)
                add(y + word)
                add(x + y + word)
                add(w + x + y + word)

def lookup(word):
    url = "https://www.xwordinfo.com/Finder?word=" + word
    headers = {"Cookie": "_ga=GA1.2.1030145848.1573942206; _gid=GA1.2.433936133.1575214547; _gat_gtag_UA_3107060_1=1; ARRAffinity=11db5d6056f4a3c8b4d3726678d908c6a84b175de3aa7f76347e78aa1465b7fa; ASP.NET_SessionId=5iopvtgbgjpfgshhwzxetjvc; WAWebSiteSID=cdb4b6ff7ff14786ad8be97db0ddd089; __gads=Test; .ASPXAUTH=00B85352516F70181FD48F12524B7C0C3C317974EC001E8D7D8F525128F4C612AE585276800A51066AFF247C092406EA5829A8B38103F37ABCC436674314C821A2702C1615EC322BA1982DB659BAE6AC792EA7E2"}
    response = requests.get(url, headers=headers)
    try:
        html = response.content.decode("utf-8")
        match = wordcount_regex.search(html)
        value = match.group(1)
        if value == "one":
            return 1
        return int(value)
    except:
        print(word)
        print(response.content)
        return 0


rootDir = '/Users/alex.rosen/personal/xword/corpora/OANC-GrAF/data/written_1/journal/slate/50'
rootDir = '/Users/alex.rosen/personal/xword/corpora/OANC-GrAF/data/'
for dirName, subdirList, fileList in os.walk(rootDir):
    print('Found directory: %s' % dirName)
    for fname in fileList:
        if fname.endswith(".txt"):
            fpath = dirName + '/' + fname
            process(fpath)

word_list = '/Users/alex.rosen/personal/xword/dicts/XwiWordList_updated345.dict'
word_list_out = '/Users/alex.rosen/personal/xword/dicts/XwiWordList_updated3456.dict'
n = 0
start = False
with open(word_list, "r") as f, open(word_list_out, "a", buffering=1) as out:
    for line in f:
        word, score = line.rstrip().split(';')
        if not start:
            if word == "stoke":
                start = True
            continue
        if score == '50' and len(word) == 6:
            corpus_count = corpus_words[word]
            nytimes_count = lookup(word)
            if len(word) == 3:
                nytimes_count /= 5
            if len(word) == 4:
                nytimes_count /= 4
            if len(word) == 5:
                nytimes_count /= 3
            if len(word) == 6:
                nytimes_count /= 2
            combined = corpus_count + nytimes_count
            if corpus_count == 0 or nytimes_count == 0:
                combined /= 2
            if combined < 1:
                score = '17'
            elif combined <= 4:
                score = '27'
            elif combined <= 10:
                score = '37'
            elif combined <= 20:
                score = '47'
            print(f"{word}\t {corpus_count} {int(nytimes_count)} {int(combined)}\t\t score={score}")
            sleep(5)

        print(word + ";" + score, file=out)
        n += 1
        if n % 1000 == 0:
            print(n)