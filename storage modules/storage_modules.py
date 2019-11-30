#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 21:24:01 2019

@author: plxiv
"""

from nltk.tokenize import word_tokenize

def store_sentences(sentences, names, languages, results_folder, person):
    for sentence in sentences:
        gender = find_pronouns(names['en'])
        if len(sentence) == len(languages):
            for i in range(len(languages)):
                with open(results_folder + 'lan_' + str(i) + '_' + gender + '.txt', 'a') as f:
                    if '\n' in sentence[i]:
                        f.write(person + ' : ' + sentence[i])
                    else:
                        f.write(person + ' : ' + sentence[i] + '\n')

def find_pronouns(filename):
    a = open(filename, 'r')
    text = a.readlines()
    text = [i for i in text if '\n' != i]
    concat_text = ' '.join(text[1:]).lower()
    tokens = word_tokenize(concat_text)
    he = len(list(filter(lambda x: x=='he' , tokens)))
    his = len(list(filter(lambda x: x=='his' , tokens)))
    she = len(list(filter(lambda x: x=='she' , tokens)))
    her = len(list(filter(lambda x: x=='her' , tokens)))
    if (he + his) > (she + her):
        gender = 'he'
    else:
        gender = 'she'
    return gender