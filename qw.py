#!/usr/bin/env python

# Notes on corpus: removed "co uk", "uv", "yuo", "du", "ye", "t v",
# "ii", "iii", "iii's"

# Code will run fine even with these back in, and it would probably be
# easier to remove them at this end

import math
import random
import re

num_spaces = 35
starts_with = 'i'
contains = ' violates fundamental'

initial = 'ittttttttttttooooooooooeeeeeeeeaaaaaaallllllnnnnnnuuuuuuiiiiiii' + \
    'sssssdddddhhhhhyyyyyrrrfffbbwwkcmvg' + num_spaces * ' '

def guess(g,x):
    x_letters = [c for c in x]
    g_letters = [c for c in g]

    for l in g_letters: x_letters.remove(l)

    g_letters.extend(x_letters)

    return ''.join(g_letters)

initial = guess(starts_with + contains,initial)

length = len(initial)

start_length = len(starts_with)
def swap_block(x):
    i = random.randint(start_length,length-1)
    j = i
    while j == i:
        j = random.randint(start_length,length-1)
    i, j = min(i,j), max(i,j)

    return x[0:i] + x[j:length] + x[i:j]

# Build word set
words = dict()
data = file('data/ngrams').read()
for word in data.split(' '):
    word = word.replace('\'','')
    if len(word) > 1:
        if not word in words:
            words[word] = 1
        else:
            words[word] = words[word] + 1

# Build 2-gram set
twograms = dict()
data = file('data/2grams')
for line in data.readlines():
    word1raw, word2raw, numraw = line.split(' ')
    word1 = word1raw.replace('\'','')
    word2 = word2raw.replace('\'','')
    num = float(numraw)
    twogram = word1 + ' ' + word2
    twograms[twogram] = num

# Build 3-gram set
threegrams = set()
data = file('data/3grams')
for line in data.readlines():
    threegrams.add(line[:-3].replace('\'',''))
    
features = [ ('ther',0.4), ('ll',0.6),
             (' i ',0.5), (' a ',0.5),
             ('ing',1.4), ('tio',0.9), ('nde',1.0), ('nd e',0.2),
             ('ent',1.1), ('ory',1.2), ('tha',0.8),
             ('ion',1.0), ('ould',1.8),
             ('ation',0.3), ('nce',0.4), ('ed t',0.4), ('tis',0.4),
             ('eory',0.8), ('ical',0.5), ('theo',0.5),
             ('th',1.2), ('er',1.1), ('on',0.9), ('an',0.7),
             ('re',0.6), ('he',0.5), ('in',0.5), ('ed',0.5),
             ('nd',0.5), ('ha',0.5), ('at',0.4), ('en',0.4),
             ('es',0.4), ('of',0.4), ('or',0.4), ('nt',0.4),
             ('ea',0.3), ('ti',0.3), ('to',0.3), ('it',0.2),
             ('st',0.2), ('io',0.2), ('le',0.2), ('is',0.2),
             ('ou',0.2), ('ar',0.2), ('as',0.2), ('de',0.2),
             ('rt',0.1), ('[a-z] [a-z]',0.3),
             ('theoretical',10.0), ]
compiled_features = [ (re.compile(pat), val) for (pat,val) in features ]

def heuristic(x):
    h = 0.0

    # features
    for (pattern, val) in compiled_features:
        count = len(pattern.findall(x))

        h = h + count * val

    # words
    x_words = x.split(' ')
    for x_word in x_words:
        if x_word in words:
            freq = 0.5 * math.floor(math.log(5 * words[x_word]))
            h = h + freq + 0.5 * len(x_word) + 0.4 * len(x_word) ** 2

    # 2-grams
    for i in range(len(x_words) - 1):
        x_2gram = x_words[i] + ' ' + x_words[i+1]
        if x_2gram in twograms:
            freq = 0.3 * math.floor(math.log(10 * twograms[x_2gram]))
            h = h + freq + 0.2 * len(x_2gram)

    # 3-grams
    for i in range(len(x_words) - 2):
        x_3gram = x_words[i] + ' ' + x_words[i+1] + ' ' + x_words[i+2]
        if x_3gram in threegrams:
            h = h + 0.2 * len(x_3gram)
            
    return h

x = initial
old_heuristic = heuristic(x)
max_heuristic = old_heuristic
for rep in range(10000000):
    new_x = swap_block(x)

    new_heuristic = heuristic(new_x)
    accept_prob = min(1.0, math.exp(-1.8 * (old_heuristic - new_heuristic)))

    if random.random() < accept_prob:
        x = new_x
        old_heuristic = new_heuristic

    if old_heuristic > max_heuristic:
        max_heuristic = old_heuristic
        print max_heuristic, x

