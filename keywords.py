#!/usr/bin/env python

"""
extract the keywords form the text files
"""

import os

from collections import defaultdict

def process(fname):
    """
    process a specific file and extract all the 1gram and 2gram words
    """
    f = open(fname, 'r')
    text = f.read()
    f.close()
    ts = []
    for ti in text.split():
        text = ti.lower()
        if not text[0].isalpha():
            text = text[1:]
        if len(text)>0 and not text[-1].isalpha():
            text = text[:-1]
        if len(text)>0:
            ts.append(text)
    # get 1grams and 2grams
    stopwords = set(['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now'])
    ngrams = defaultdict(int)
    for ti in range(len(ts)-1):
        word1 = ts[ti]
        word2 = ts[ti+1]
        words = word1+" "+word2
        if word1 not in stopwords:
            ngrams[word1] += 1
        if word1 not in stopwords and word2 not in stopwords:
            ngrams[words] += 1
    if ts[-1] not in stopwords:
        ngrams[ts[-1]] += 1
    #
    return ngrams

def get_keywords(dname):
    """
    get the keywords from all the files in the directory
    """
    ngrams = defaultdict(int)
    for fi in os.listdir(dname):
        fname = '%s/%s' % (dname, fi)
        words = process(fname)
        for k,v in words.items():
            ngrams[k] += v
    # sort
    for w in sorted(ngrams, key=ngrams.get, reverse=True):
        print w, ngrams[w]


if __name__ == '__main__':
    get_keywords('./text')