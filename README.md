# GebioToolkit

We present the GebioToolkit for extracting multilingual parallel corpora at sentence level, with document and gender information from Wikipedia biographies. Despite the gender inequalities present in Wikipedia, the toolkit has been designed to extract corpus balanced in gender. 
While our toolkit is able to customize the languages for which we are extracting the multilingual corpus, in this work, we extracted a corpus of 2000 sentences in English, Spanish and Catalan, which has been post-edited by native speakers to be valid as test dataset for machine translation.

## Dependencies

* Python 3.6
* Numpy, tested with 1.16.4
* LASER (https://github.com/facebookresearch/LASER)

## Usage

### Corpus extractor

_Change domain_

If we want to change the domain of gebiotoolkit, we need to generate new files and delete the ones from the folder dictionary_of_files. To generate new ones, we need to get a list of wikipedia entries, the easiest way to achieve this is by using the petscan tool (https://petscan.wmflabs.org/) in which allows you to perform it easily. Next we execute the following code:

    python3 wp_api_language_search.py -csv new_list.csv 




## References

For more information, please check https://arxiv.org/pdf/1912.04778.pdf

