#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 23:34:57 2019

@author: plxiv
"""

from scipy import spatial
import numpy as np
from embed_extractor import extract
import time
import os
os.environ['LASER'] = '/home/plxiv/LASER/LASER-master/'
LASER = os.environ['LASER']


def mine(src, trg, src_lang, trg_lang, src_embeddings, trg_embeddings, output, mode, remove=False):
    mine_file =LASER + 'source/mine_bitexts.py'
    os.system('python3 ' + mine_file + ' ' +  
    src + ' ' + trg + ' ' +
    '--src-lang ' + src_lang + ' ' + 
    '--trg-lang ' + trg_lang + ' ' +
    '--src-embeddings ' + src_embeddings + ' ' +
    '--trg-embeddings ' + trg_embeddings + ' ' +
    '--output ' + output + ' ' +
    '--mode ' + mode)
    try:
        with open(output, 'r', encoding='utf8') as f:
            parallel = f.readlines()
        for i,j in enumerate(parallel):
            parallel[i] = j.split('\t')
        os.remove(output)
    except:
        parallel = []
    return parallel

def test():
    models = 'models/'
    embeds = 'embeds/'
    encoder= LASER + models + 'bilstm.93langs.2018-12-26.pt'
    bpe_codes = LASER + models + '93langs.fcodes'    
    
    lang_src = 'en'
    lang_trg = 'fi'
    file_src = 'en'
    file_trg = 'fin'
    output_src = embeds + lang_src
    output_trg = embeds + lang_trg
    
    en = extract(encoder, lang_src, bpe_codes, file_src, output_src)
    fi = extract(encoder, lang_trg, bpe_codes, file_trg, output_trg)  
    
    parallel_file = 'parallel.txt'
    parallel_sentences = mine(file_src, file_trg, lang_src, lang_trg, output_src, output_trg, parallel_file, 'mine')
  

if __name__ == '__main__':   
    test()
