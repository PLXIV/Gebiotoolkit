#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 20:37:13 2019

@author: plxiv
"""

import os
import sys
os.environ['LASER'] = '/home/plxiv/LASER/LASER-master/'
LASER = os.environ['LASER']
sys.path.append(LASER + 'source/')
sys.path.append(LASER + '/source/lib')

from text_processing import Token, BPEfastApply
from embed import SentenceEncoder, EncodeFile, EmbedLoad
import numpy as np
import tempfile


def extract(encoder, token_lang, bpe_codes, ifname, output, remove= False , verbose = False):
    with tempfile.TemporaryDirectory() as tmpdir:
#        ifname = ''  
        if token_lang != '--':
            tok_fname = os.path.join(tmpdir, 'tok')
            Token(ifname,
                  tok_fname,
                  lang=token_lang,
                  romanize=True if token_lang == 'el' else False,
                  lower_case=True, gzip=False,
                  verbose=verbose, over_write=False)
            ifname = tok_fname
        if bpe_codes:
            bpe_fname = os.path.join(tmpdir, 'bpe')
            BPEfastApply(ifname,
                         bpe_fname,
                         bpe_codes,
                         verbose=verbose, over_write=True)
            ifname = bpe_fname
        EncodeFile(encoder,
                   ifname,
                   output,
                   verbose=verbose, over_write=False,
                   buffer_size=10000)
        return EmbedLoad(output)

def generate_encoder(encoder_file):
    return SentenceEncoder(encoder_file,
                              max_sentences=None,
                              max_tokens=12000,
                              sort_kind='quicksort',
                              cpu=True)
def test():
    models = 'models/'
    embeds = 'embeds/'
    encoder_file= LASER + models + 'bilstm.93langs.2018-12-26.pt'
    bpe_codes = LASER + models + '93langs.fcodes'    
    
    lang_src = 'en'
    lang_trg = 'fi'
    file_src = 'en'
    file_trg = 'fin'
    output_src = embeds + lang_src
    output_trg = embeds + lang_trg
    encoder = generate_encoder(encoder_file)
    en = extract(encoder, lang_src, bpe_codes, file_src, output_src)
    return en

if __name__ == '__main__':    
    en = test()

    