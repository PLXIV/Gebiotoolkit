#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 23:34:57 2019

@author: plxiv
"""
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