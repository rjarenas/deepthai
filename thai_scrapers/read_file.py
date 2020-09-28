# -*- coding: utf-8 -*-
"""
Created on Sat Sep 19 01:14:38 2020

@author: Ruben
"""
from pythainlp import tokenize
from pythainlp.util import isthai
import pandas as pd

text = pd.read_csv("th_wikipedia_org.csv")

dictionary = {()}
corpus = []

# Parallize this
for i in range(300):
    tokens = tokenize.word_tokenize(text.text[i], engine = 'deepcut', keep_whitespace = False)
    
    # Remove punctuation and white space
    
    # Remove non-thai words and stop words
    
    # Retokenize
    
    dictionary.update(tokens)
    paragraphs.append(tokens)

thai_words = 0
other_words = []
for s in dictionary:
    if isthai(s):
        thai_words = thai_words + 1
    else:
        other_words.append(s)