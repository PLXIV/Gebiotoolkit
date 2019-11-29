import os
import ast
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class File_selection(object):
    def __init__(self, dictionary_of_names, languages, debug = False):
        self.dictionary_of_names = dictionary_of_names
        self.languages = self.select_languages(languages)
        self.people = self.read_people()
        self.selected_people = self.find_selected_languages(self.languages)
        if debug:
            self.all_languages = self.find_languages()
            self.acronims, self.values, self.quantities = self.find_language_quantities()

    def read_people(self):
        people = {}
        counter = 1
        for l in os.listdir(self.dictionary_of_names):
            if 'dictionary_of_names' in l:
                file = open(self.dictionary_of_names + l,'r')
                for i in file:
                    if len(i) > 2:
                        t = ast.literal_eval(i)
                        if type(t) is not float:
                            people[t[2]] = t[3]
                        else:
                            print('reading dictionary_of_names files... ', counter)
                            counter +=  1
        return people

    def find_selected_languages(self, languages):
        selected_people = {}
        for k, v in self.people.items():
            selected_languages = []
            if v:
                for lan in v:                    
                    if lan[0] in languages:
                        selected_languages.append(lan)
                if len(selected_languages) == len(languages):
                    selected_people[k] = selected_languages
        return selected_people

    def select_languages(self, languages):
        selected_languages = []
        if not languages:
            selected_languages = self.find_languages()
        else:
            selected_languages = languages
        return selected_languages
    
    def find_languages(self):
        languages_acronim = []
        for k,v in self.people.items():
            if v:
                for lan in v:
                    if lan[0] not in languages_acronim:
                        languages_acronim.append(lan[0])
        return languages_acronim
    
    def find_language_quantities(self):
        num_languages = []
        for acronim in self.all_languages:
            if len(acronim) < 5:
                num_languages.append([int(len(self.find_selected_languages([acronim]))), acronim])
        num_languages.sort(reverse = True)
        num_languages = np.array(num_languages)
        values = num_languages[:,0].astype(int)
        acronims = num_languages[:,1]
        return acronims, values, num_languages
    
    def plot_quantities(self, num_languages):
        plt.rcdefaults()
        fig, ax = plt.subplots()
        y_pos = np.arange(num_languages)
        error = np.random.rand(num_languages)
        ax.barh(y_pos, self.values[:num_languages], xerr=error, align='center', color='gray')
        ax.tick_params(direction='out', length=6, width=2, labelsize='28',
               grid_color='r', grid_alpha=0.5)
        ax.set_yticks(y_pos)
        ax.set_ylabel('Languages', fontsize=28, position=(1.0, 0.5))
        ax.set_xlabel('Wikipedia entries', fontsize=28)
        ax.set_yticklabels(self.acronims[:num_languages])
        ax.invert_yaxis()  # labels read top-to-bottom

    def generate_table(self):
        f = open("plots/table", "w")
        f.write(pd.DataFrame.to_latex(pd.DataFrame(self.quantities)))
        f.close()
        

def main():
    dictionary_of_names = 'dictionary_of_names/' 
    debug = False
    gen_table = False
    gen_plot = False
    languages = []
    r = File_selection(dictionary_of_names, languages, debug = True)
    if debug:
        if gen_table:
            r.generate_table()
        if gen_plot:
            r.plot_quantities(20)

if __name__ == '__main__':
    main()

    
