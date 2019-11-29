#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 21:13:52 2019

@author: plxiv
"""

import nltk.data

def preprocess(outputfile, filename):
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    tmp = 'preprocessed/'
    write = open(tmp + outputfile, 'a')
    with open(filename, 'r') as f:
        a = f.readlines()
    for i in range(3,len(a)-1):
        if len(a[i]) > 15:
            b = tokenizer.tokenize(a[i])
            for c in b:
                write.write(c + '\n')
