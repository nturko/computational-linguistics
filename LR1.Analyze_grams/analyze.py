import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

class Analyze(object):
    def __init__(self, author, books_list):
        self.name = author
        self.books = books_list
        self.bigram_matrix = np.array([[0]*33]*33)
        self.string_alphabet = 'абвгґдеєжзийклмнопрстуфхцчшщіїьюя'
        self.ukrainian_freq_dict = {'а': 0.0807, 'б': 0.0177, 'в': 0.0545, 'г': 0.0154, 'ґ': 0.0001, 'д': 0.0338, 'е': 0.0338, 'є': 0.0061, 
                            'ж': 0.0093, 'з': 0.0232, 'и': 0.0626, 'й': 0.0116, 'к': 0.0354, 'л': 0.0369, 'м': 0.0303, 'н': 0.0681, 
                            'о': 0.0942, 'п': 0.0290, 'р': 0.0448, 'с': 0.0424, 'т': 0.0535, 'у': 0.0336, 'ф': 0.0028, 'х': 0.0119, 
                            'ц': 0.0083, 'ч': 0.0141, 'ш': 0.0076, 'щ': 0.0056, 'і': 0.0575, 'ї': 0.0065, 'ь': 0.0177, 'ю': 0.0061,
                            'я': 0.0248, ' ': 0.175}
        self.alphabet_dict = dict()
        self.alphabet_freq_dict = dict()
        self.bigram_dict = dict()
        self.bigram_freq_dict = dict()
        self.col_name = []
        self.row_name = []
        for i in self.string_alphabet:
            self.alphabet_dict[i] = 0
            self.col_name.append(i)
            self.row_name.append(i)
        self.alphabet_dict[' '] = 0
        self.count_symbols = 0


    def symbol_analyze(self, result_file, flag):
        for text in self.books:
            for letter in text.lower():
                if letter in self.alphabet_dict:
                    self.alphabet_dict[letter] += 1
                    self.count_symbols += 1
        
        for letter in self.alphabet_dict:
            self.alphabet_freq_dict[letter] = round(self.alphabet_dict[letter]/self.count_symbols, 4)  
        if flag is True:        
            plt.bar(self.alphabet_freq_dict.keys(), self.alphabet_freq_dict.values())
            plt.title(f'Гістограма частот символів для автора {self.name}. К-сть символів: {self.count_symbols}')
            plt.show()
        result_file.write(str(self.alphabet_freq_dict))

    
    def symbol_substraction(self):
        difference_dict = self.alphabet_freq_dict
        for letter in difference_dict:
            difference_dict[letter] = abs(difference_dict[letter] - self.ukrainian_freq_dict[letter])

        plt.bar(difference_dict.keys(), difference_dict.values())
        plt.title(f'Гістограма різниці частот автора {self.name}')
        plt.show()


    def bigram_analyze(self, result_file):
        for text in self.books:
            for i in range(len(text)-1):
                symbol = text[i].lower()
                next_symbol = text[i+1].lower()
                if symbol != ' ' and next_symbol != ' ':
                    if symbol in self.alphabet_dict and next_symbol in self.alphabet_dict:
                        bigram = symbol + next_symbol
                        if bigram in self.bigram_dict:
                            self.bigram_dict[bigram] += 1    
                        else:
                            self.bigram_dict[bigram] = 1
        
        for bigram in self.bigram_dict:
            self.bigram_freq_dict[bigram] = round(self.bigram_dict[bigram]/self.count_symbols, 4)

        result_file.write(str(sorted(self.bigram_freq_dict.items()))) 
    
    def heat_map(self):
        for first in self.string_alphabet:
            for second in self.string_alphabet:
                key = first + second
                if key in self.bigram_dict:
                    i = self.string_alphabet.index(first)
                    j = self.string_alphabet.index(second)
                    self.bigram_matrix[i][j] = self.bigram_dict[key]

        sns.heatmap(pd.DataFrame(data=self.bigram_matrix, columns=self.col_name, index=self.row_name)).invert_yaxis()
        plt.title(f'Теплова діаграмма біграм автора: {self.name}')
        plt.show()
