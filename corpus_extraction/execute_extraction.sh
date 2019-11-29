#!/bin/sh
cd ..
for i in {0..9}
do
    python3 wp_api_language_search.py -v $i > dictionary_of_names_2/dictionary_of_names_$i.txt &
done

