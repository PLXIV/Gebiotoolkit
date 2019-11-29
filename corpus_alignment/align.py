#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  6 02:03:01 2019

@author: plxiv
"""
import os
import sys
import nltk.data
sys.path.insert(0, '/home/plxiv/tfm/Resources_for_gender_bias_NLP/corpus_extractor/')
os.environ['LASER'] = '/home/plxiv/LASER/LASER-master/'
LASER = os.environ['LASER']

from embed_extractor import extract, generate_encoder
from parallel_extractor import mine
from people_selection import People_selection
from nltk.tokenize import word_tokenize


def find_file(folder, target):
    files = os.listdir(folder)
    results = 'Not found'
    for filename in files:
        if target in filename:
            results = filename
    return results

def obtain_all_filenames(corpus_folder, languages):
    dict_files = {}
    for i in languages:
        dict_files[i] = os.listdir(corpus_folder + i  + '/raw/')
    return dict_files

def extract_filenames(dict_filenames, corpus_folder, person, list_languages):
    names = {}
    if person in dict_filenames['en']:
        names['en'] = corpus_folder + 'en' + '/raw/' + person
        for lan_p in list_languages:
            fn = lan_p[1].split(' – ')[0]
            if fn in dict_filenames[lan_p[0]]:
                names[lan_p[0]] = corpus_folder + lan_p[0] + '/raw/' +  fn
    return names

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
        else:
            with open('wrong.txt', 'a') as f:
                f.write(str(sentence))

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

def remove_tmp(languages):
    for i in languages:
        try:
            os.remove('preprocessed/' + i)
            os.remove('embeds/' + i)
        except:
            pass

def check_language(lan):
    if lan == 'ar':
        lan_fol = 'ara'
    elif lan == 'ja':
        lan_fol = 'jpn'
    else:
        lan_fol = lan
    return lan_fol

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

def find_selected_sentences(languages, names, encoder, bpe_codes, embeds, parallel_file, threshold):
    sel_par_sentences= []
    all_embeds = []
    for lan in languages:
        preprocess(lan, names[lan])
        lan_fol = check_language(lan)
        all_embeds.append(extract(encoder, lan_fol, bpe_codes, 'preprocessed/' + lan, embeds + str(lan), remove= True, verbose = False))
    for lan in languages:
        lan_fol = check_language(lan)
        all_par_sentences = mine('preprocessed/' + languages[0], 
                                 'preprocessed/' + lan, 
                                 languages[0], lan_fol, 
                                 embeds + languages[0], embeds + lan, 
                                 parallel_file, 'mine')
        if all_par_sentences:
            for i, par in enumerate(all_par_sentences):
                if float(par[0]) < threshold:
                    break
            sel_par_sentences.append(all_par_sentences[:i])
    remove_tmp(languages)
    return sel_par_sentences

def compare_sentences(lan_1, lan_2):
    same_lan = [i[1] for i in lan_2]
    update = []
    for i, sentence in enumerate(lan_1):
        if sentence[0] in same_lan:
            lan_1[i].append(lan_2[same_lan.index(sentence[0])][2])
            update.append(lan_1[i])
    return update

def extract_parrallel(sel_par_sentences):
    try:
        parrallel_sentences = [[i[1]] for i in sel_par_sentences[0]]
        for i in range(1,len(sel_par_sentences)):
            parrallel_sentences = compare_sentences(parrallel_sentences, sel_par_sentences[i])
    except:
        parrallel_sentences = []
    return parrallel_sentences        

def run(encoder, corpus_folder, names, languages, threshold = 1.055):
    embeds = 'embeds/'
    bpe_codes = LASER + 'models/93langs.fcodes'  
    parallel_tmp = 'parallel.txt'
    sel_par_sentences = find_selected_sentences(languages, names, encoder, bpe_codes, embeds, parallel_tmp, threshold)   
    par = extract_parrallel(sel_par_sentences)
    return par

def main():
    corpus_folder = '/media/plxiv/AEF0C4B1F0C480D7/tmp/Resources_for_gender_bias_NLP/corpus_extractor/output/'
    languages = ['es','ca']
    results_folder = 'results/'
    p_all = '/home/plxiv/tfm/Resources_for_gender_bias_NLP/corpus_extractor/p_all/'
    encoder_file = LASER + 'models/bilstm.93langs.2018-12-26.pt'
    encoder = generate_encoder(encoder_file)
    people = People_selection(p_all, languages).selected_people
    languages = ['en'] + languages
    dict_filenames =  obtain_all_filenames(corpus_folder, languages)
    counter = 18497
    a = list(people.items())
    print(len(a))
    a = a[counter:]
    for person, list_languages in a:
        counter+=1
        print(counter)
        names = extract_filenames(dict_filenames, corpus_folder, person, list_languages)
        if len(names.keys()) == len(languages):
            sentences = run(encoder, corpus_folder, names, languages)
            if sentences:
                store_sentences(sentences, names, languages, results_folder, person)
    
if __name__ == '__main__':   
    main()
