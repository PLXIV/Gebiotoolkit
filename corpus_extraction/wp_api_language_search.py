#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 00:22:09 2019

@author: plxiv
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import wikipedia
import argparse
import time

def retrieve_args():
    parser = argparse.ArgumentParser(description='Finds the different languages available for an specific wikipedia article')
    parser.add_argument('-v','--vr_number', required=False, help='virtual machine assigned. Must be lower than the total number of virtual machines', default= '1')
    parser.add_argument('-t','--total', required=False, help='total of processes created', default='1')
    parser.add_argument('-c','--csv', required=False, help='folder which contains names of living people', default='csv/dF7mxWq4.csv')
    args = parser.parse_args()
    return args

def main():
    args = retrieve_args()
    vr_number = int(args.vr_number)
    total_vr = int(args.total)

    initial_time = time.time()

    df=pd.read_csv(args.csv, sep=',',header=None)
    all_p = []
    for person in df.values[1:,1]:
        person = person.replace("\\",'')
        all_p.append(person.replace('_',' '))
    fold_size = int(len(all_p) / total_vr)

    if vr_number == 1:
        ini = 0
    else:
        ini = fold_size*vr_number

    call_api(vr_number, all_p[ini:ini+fold_size])
    print(time.time() - initial_time)

def call_api(cpu, names):
    counter = 0
    for i in names:
        t_sample = time.time()
        links = None
        number_of_tries = 0
        while links is None and number_of_tries < 10:
            try:
                original_link = wikipedia.page(i)
                soup = BeautifulSoup(urlopen(original_link.url))
                links = [[el.get('lang'), el.get('title')] for el in soup.select('li.interlanguage-link > a')]
            except:
                number_of_tries += 1
        counter +=1
        print(str((t_sample - time.time(), counter, i, links)) + '\n' , flush=True)

if __name__ == '__main__':
    main()
