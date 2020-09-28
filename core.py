# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 14:01:49 2020

@author: Ruben
"""
from pythainlp import tokenize
from pythainlp.util import isthai, normalize
from num2words import num2words
import re
import numpy as np
import pandas as pd

def process_corpus(corpus, number_token = "<NUM>", oov_token = "<OOV>"):
    # Create an empty dictionary and token list
    dictionary = {oov_token : 1}
    tokenized_corpus = []
    
    corpus = corpus[1:1000]
    
    for entry in corpus:
        # Normalize the entry
        entry = normalize(entry)
        
        # Tokenize each entry
        tokens = np.array(tokenize.word_tokenize(entry, engine = 'newmm', keep_whitespace = False))
                
        # Remove non-Thai words
        tokens = tokens[[isthai(t, ignore_chars = "0123456789") and t != "" for t in tokens]]
            
        # Replace numbers with text
        #tokens = [re.sub("^\d*$",num2words(t, lang = 'th'),t) for t in tokens] 
        
        # Add the tokens to the tokenized corpus
        tokenized_corpus.append(tokens)
        
        # Add the tokens to the dictionary and increment counts
        for t in tokens:
            if t in dictionary:
                dictionary[t] = dictionary[t] + 1
            else:
                dictionary[t] = 1

    return tokenized_corpus, dictionary

filename = "thai_scrapers/sanook_co_th.csv"
corpus = pd.read_csv(filename)
corpus = np.array(corpus.text)

tokenized_corpus, dictionary = process_corpus(corpus)
    