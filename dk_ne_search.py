#!/usr/bin/env python
#
# Extract entities from DataKind blog using generic NER
# courtesy of http://pixelmonkey.org/pub/nlp-training/

import bs4
import feedparser
import nltk
import string
import types

RSS_PATH = 'http://www.datakind.org/blog/feeds/rss/'

def get_text(post):
    return bs4.UnicodeDammit(post.summary).unicode_markup

def text2tree(text):
    chunks = \
        nltk.ne_chunk(
            nltk.pos_tag(
                nltk.word_tokenize(text)),
        binary=True) # binary only enables one type, "NE"
    return chunks

def chunk2entity(chunk):
    return ' '.join(leaf[0] for leaf in chunk.leaves())

def tree2entities(tree):
    # set comprehension, what the fuck up!?
    entities = {
        chunk2entity(chunk)
        for chunk in tree
        if 'node' in dir(chunk)
    }
    # yea!
    return entities

def get_names(text):
    return tree2entities(text2tree(text))

feed = feedparser.parse(RSS_PATH)

print [feed['feed'][k] for k in ('link', 'updated')]

texts = [get_text(post) for post in feed.entries]

names = reduce(lambda s1,s2: s1 | s2, [get_names(text) for text in texts])

print '\n'.join(sorted([n.encode('UTF-8') for n in names]))
