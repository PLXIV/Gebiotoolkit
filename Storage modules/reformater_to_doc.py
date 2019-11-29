#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 00:46:36 2019

@author: plxiv
"""

import os
import re
import sys
import pickle
from urllib.request import urlopen
from bs4 import BeautifulSoup
import wikipedia

def id_retriever(name, lan):
    if lan != 'en':
        wikipedia.set_lang("en")
        page = wikipedia.page(name)
        soup = BeautifulSoup(urlopen(page.url))
        for el in soup.select('li.interlanguage-link > a'):
            if lan == el.get('lang'):
                pagename = el.get('title').split(' – ')[0]
        wikipedia.set_lang(lan)
    else:
        pagename = name
    page = wikipedia.page(pagename)
    idd = page.pageid
    print(idd)
    return idd

def include_sentence(sens):
    name = sens.split(':')[0]
    valid_sentence = re.sub(name + ': ','',sens)
    valid_sentence = re.sub('\n','',valid_sentence)
    return valid_sentence, name[:len(name)-1]

def store_sentence(filestore, name, all_sentences,lan, gender):
    seg = 1 
    idd = id_retriever(name, lan)
    filestore.write('<doc docid="' + name +'" wpid="' + idd + '" language="' + lan + '" topic="" gender="' + gender + '">\n')
    filestore.write('<title> ' + name + '</title>\n')
    for z in all_sentences:
        filestore.write('<seg id="' + str(seg) + '">' + z + '<\seg>\n')
        seg +=1
    filestore.write('</doc>\n')


def main():
    corpus = sys.argv[1]
    gender = sys.argv[3]
    lan = sys.argv[4]

    all_sentences = []      
    with open(corpus) as f:
        sentences = f.readlines()

    valid_sentence, name = include_sentence(sentences[0])
    all_sentences.append(valid_sentence)

    count = 0
    for j in range(1,len(sentences)):
        sens = sentences[j]
        valid_sentence, current_name = include_sentence(sentences[j])
        if name == current_name:
            all_sentences.append(valid_sentence)
        else:
            filestore = open(sys.argv[2], 'a')
            if name in b.keys():
                store_sentence(filestore, name, all_sentences,lan, gender)
                count +=1

            name = current_name #Reset and store values for the new person
            all_sentences = []
            all_sentences.append(valid_sentence)
            filestore.close()  

    #last sample
    filestore = open(sys.argv[2], 'a')
    store_sentence(filestore, name, all_sentences,lan, gender, b)
    filestore.close()  
    count +=1
    print(count)

if __name__ == '__main__':   
    main()
