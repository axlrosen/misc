from nltk.corpus import brown
import nltk

def get_tagger(n: int):
    fd = nltk.FreqDist(brown.words(categories='news'))
    cfd = nltk.ConditionalFreqDist(brown.tagged_words(categories='news'))
    most_freq_words = fd.most_common(n)
    likely_tags = dict((word, cfd[word].max()) for (word, _) in most_freq_words)
    return nltk.UnigramTagger(model=likely_tags)
