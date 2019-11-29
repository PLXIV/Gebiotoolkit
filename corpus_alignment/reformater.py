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

def load_categories(previous_file):
    with open(previous_file,'rb') as f:
        a = f.readlines()
    b = {}    
    for i in a:
        c = i.decode('utf-8')
        if '<doc docid=' in c:
            d = c.split('topic="')
            val = d[1].split('"')[0]
            e = d[0].split('"')[1]
            b[e] = val
    return b

def store_sentence(filestore, name, all_sentences,lan, gender, b):
    seg = 1 
    topic = b[name]
    idd = id_retriever(name, lan)
    filestore.write('<doc docid="' + name +'" wpid="' + idd + '" language="' + lan + '" topic="' + topic +  '" genre="' + gender + '">\n')
    filestore.write('<title> ' + name + '</title>\n')
    for z in all_sentences:
        filestore.write('<seg id="' + str(seg) + '">' + z + '<\seg>\n')
        seg +=1
    filestore.write('</doc>\n')
    
    
if __name__ == '__main__':   
    corpus = sys.argv[1]
    gender = sys.argv[3]
    lan = sys.argv[4]
    
    all_sentences = []      
    with open(corpus) as f:
        sentences = f.readlines()

    b = load_categories('she.1000.doc.ca')
    print(b)
    valid_sentence, name = include_sentence(sentences[0])
    all_sentences.append(valid_sentence)
    
    count = 0
    for j in range(1,len(sentences)):
        sens = sentences[j]
        valid_sentence, current_name = include_sentence(sentences[j])
        if name == current_name: #if the person is the same as the previous sentence - append to a list
            all_sentences.append(valid_sentence)
        else: #when it detects that the sentence is referecing another person - store all values from the list in the desired format
            filestore = open(sys.argv[2], 'a')
            if name in b.keys():
                store_sentence(filestore, name, all_sentences,lan, gender, b)
                count +=1
            else:
                print(name)
           
            #Reset and store values for the new person
            name = current_name
            all_sentences = []
            all_sentences.append(valid_sentence)
            filestore.close()  
    

    #last sample    
    filestore = open(sys.argv[2], 'a')
    store_sentence(filestore, name, all_sentences,lan, gender, b)
    filestore.close()  
    count +=1
    print(count)
    