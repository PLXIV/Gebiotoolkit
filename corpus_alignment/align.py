#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  6 02:03:01 2019

@author: plxiv
"""
import os
import pickle
import argparse
from storage_modules import store_sentences
from preprocess import preprocess
from embed_extractor import extract, generate_encoder
from parallel_extractor import mine
os.environ['LASER'] = '/home/plxiv/LASER/LASER-master/'
LASER = os.environ['LASER']

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

def remove_tmp(languages):
    for i in languages:
        try:
            os.remove('preprocessed/' + i)
            os.remove('embeds/' + i)
        except:
            pass

def extract_candidate_sentences(languages, names, encoder, bpe_codes, parallel_file, threshold):
    sel_par_sentences= []
    all_embeds = []
    for lan in languages:
        preprocess(lan, names[lan])
        all_embeds.append(extract(encoder, lan, bpe_codes, 'preprocessed/' + lan, 'embeds/' + str(lan), remove= True, verbose = False))
    for lan in languages:
        all_par_sentences = mine('preprocessed/' + languages[0], 
                                 'preprocessed/' + lan, 
                                 languages[0], lan, 
                                 'embeds/' + languages[0], 'embeds/' + lan, 
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

def find_parallel_sentences(sel_par_sentences):
    try:
        parrallel_sentences = [[i[1]] for i in sel_par_sentences[0]]
        for i in range(1,len(sel_par_sentences)):
            parrallel_sentences = compare_sentences(parrallel_sentences, sel_par_sentences[i])
    except:
        parrallel_sentences = []
    return parrallel_sentences        

def run(encoder, corpus_folder, names, languages, threshold = 1.055):
    bpe_codes = LASER + 'models/93langs.fcodes'  
    parallel_tmp = 'parallel.txt'
    sel_par_sentences = extract_candidate_sentences(languages, names, encoder, bpe_codes, parallel_tmp, threshold)   
    par = find_parallel_sentences(sel_par_sentences)
    return par

def retrieve_args():
    parser = argparse.ArgumentParser(description='Generates a pickle in which contains the dictionary of the samples in which all languages have the same entry')
    parser.add_argument('-l','--languages', nargs='+', required=True, help='Languages in which the parallel sentences will be generated')
    parser.add_argument('-f','--folder', required=True, help='root folder where the extracted corpus is stored')
    parser.add_argument('-p','--pickle', required=True, help='pickle that contains the people selection')
    parser.add_argument('-s','--save_path', required=False, help='Folder where the sentences will be stored', default='results/')
    parser.add_argument('-e','--encoder', required=False, help='path to the LASER encoder', default='/home/plxiv/LASER/LASER-master/models/bilstm.93langs.2018-12-26.pt')
    args = parser.parse_args()
    return args

def main():
    args = retrieve_args()
    corpus_folder = args.folder
    languages = args.languages
    results_folder = args.save_path
    encoder_file = args.encoder
    encoder = generate_encoder(encoder_file)
    with open(args.pickle, 'rb') as f:
        people = pickle.load(f)
    dict_filenames =  obtain_all_filenames(corpus_folder, languages)
    for person, list_languages in people.items():
        names = extract_filenames(dict_filenames, corpus_folder, person, list_languages)
        if len(names.keys()) == len(languages):
            sentences = run(encoder, corpus_folder, names, languages)
            if sentences:
                store_sentences(sentences, names, languages, results_folder, person)
    
if __name__ == '__main__':   
    main()
