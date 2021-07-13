from analyze import *

def main():
   with open('books_source/gogol_viy.txt', 'r' ) as f:
      gogol_book_1 =  f.read()
      f.close()
    
   with open('books_source/gogol_vechori_na_hytori.txt', 'r') as f:
      gogol_book_2 =  f.read()
      f.close()
   
   with open('books_source/gogol_nich.txt', 'r') as f:
      gogol_book_3 =  f.read()
      f.close()
    

   gogol_books = [gogol_book_1, gogol_book_2, gogol_book_3]

   gogol_symbols_result = open('analyze_results/gogol_symbols_result_1.txt', 'w')
   gogol_bigram_result = open('analyze_results/gogol_bigram_result_1.txt', 'w')
    
   gogol = Analyze(author='М. Гоголь', books_list=gogol_books)
   gogol.symbol_analyze(gogol_symbols_result, False)
   gogol.bigram_analyze(gogol_bigram_result)
   # gogol.heat_map()
   # gogol.symbol_substraction()

#--------------------------------------------------------------------------------------------------------------------------------------------#

   with open('books_source/nechui_netoi.txt', 'r') as f:
      nechui_book_1 =  f.read()
      f.close()
    
   with open('books_source/nechui_kaidash.txt', 'r') as f:
      nechui_book_2 =  f.read()
      f.close()
   
   with open('books_source/nechui_kniaz.txt', 'r') as f:
      nechui_book_3 =  f.read()
      f.close()

   
   nechui_books = [nechui_book_1, nechui_book_2, nechui_book_3]

   nechui_symbols_result = open('analyze_results/nechui_symbols_result_1.txt', 'w')
   nechui_bigram_result = open('analyze_results/nechui_bigram_result_1.txt', 'w')
    
   nechui = Analyze(author='І. Нечуй-Левицький', books_list=nechui_books)
   nechui.symbol_analyze(nechui_symbols_result, False)
   nechui.bigram_analyze(nechui_bigram_result)
   # nechui.heat_map()
   # nechui.symbol_substraction()
    

#--------------------------------------------------------------------------------------------------------------------------------------------#

   with open('books_source/nestaiko_toreadori.txt', 'r') as f:
      nestaiko_book_1 =  f.read()
      f.close()
    
   with open('books_source/nestaiko_odunica.txt', 'r') as f:
      nestaiko_book_2 =  f.read()
      f.close()
   
   with open('books_source/nestaiko_zaichiki.txt', 'r') as f:
      nestaiko_book_3 =  f.read()
      f.close()

   
   nestaiko_books = [nestaiko_book_1, nestaiko_book_2, nestaiko_book_3]

   nestaiko_symbols_result = open('analyze_results/nestaiko_symbols_result_1.txt', 'w')
   nestaiko_bigram_result = open('analyze_results/nestaiko_bigram_result_1.txt', 'w')
    
   nestaiko = Analyze(author='В. Нестайко', books_list=nestaiko_books)
   nestaiko.symbol_analyze(nestaiko_symbols_result, False)
   nestaiko.bigram_analyze(nestaiko_bigram_result)
   # nestaiko.heat_map()
   # nestaiko.symbol_substraction()

#--------------------------------------------------------------------------------------------------------------------------------------------#

   authors_bigram_comprassion(gogol, nechui)
   authors_bigram_comprassion(nechui, gogol)
   authors_bigram_comprassion(gogol, nestaiko)
   authors_bigram_comprassion(nechui, nestaiko)

#--------------------------------------------------------------------------------------------------------------------------------------------#

   with open('books_source/gogol_vechir.txt', 'r') as f:
      gogol_unknow_book =  f.read(50000)
      f.close()

   gogol_unknow_symbols = open('analyze_results/gogol_unknown_result.txt', 'w')
   gogol_unknow_bigram = open('analyze_results/gogol_unknown_bigram.txt', 'w')
   
   unknown_gogol = Analyze(author='Невідомий', books_list=[gogol_unknow_book])
   unknown_gogol.symbol_analyze(gogol_unknow_symbols, False)
   unknown_gogol.bigram_analyze(gogol_unknow_bigram)

   authors_symbol_density = [gogol.alphabet_freq_dict, nechui.alphabet_freq_dict, nestaiko.alphabet_freq_dict]
   authors_bigram_density = [gogol.bigram_freq_dict, nechui.bigram_freq_dict, nestaiko.bigram_freq_dict]
   authors_names = [gogol.name, nechui.name, nestaiko.name]

   #guess_book_symbols(unknown_gogol.alphabet_freq_dict, authors_symbol_density, authors_names) # symbol guessing
   #guess_book_symbols(unknown_gogol.bigram_freq_dict, authors_bigram_density, authors_names) # bigram guessing

#--------------------------------------------------------------------------------------------------------------------------------------------#

def authors_bigram_comprassion(author1, author2):
   author1_bigram = author1.bigram_freq_dict
   author2_bigram = author2.bigram_freq_dict
   
   string_alphabet = 'абвгґдеєжзийклмнопрстуфхцчшщіїьюя'
   bigram_matrix = np.array([[.0]*33]*33)
   for first in string_alphabet:
      for second in string_alphabet:
         key = first + second
         i = string_alphabet.index(first)
         j = string_alphabet.index(second)
         if key in author1_bigram and key in author2_bigram:
            bigram_matrix[i][j] = abs(author1_bigram[key]-author2_bigram[key])
         elif key in author1_bigram and author1_bigram[key] != .0:
               bigram_matrix[i][j] = author1_bigram[key]
         elif key in author2_bigram and author2_bigram[key] != .0:
               bigram_matrix[i][j] = author2_bigram[key]


   sns.heatmap(pd.DataFrame(data=bigram_matrix, columns=author1.col_name, index=author1.row_name)).invert_yaxis()
   plt.title(f'Теплова діаграмма різниці використання пар літер між авторами: {author1.name} & {author2.name}')
   plt.show()

#--------------------------------------------------------------------------------------------------------------------------------------------#

def guess_book_symbols(unknow_book_density, density_list, authors_list):
   density_diff = [.0]*len(density_list)

   for i in range(len(density_list)):
      for letter in unknow_book_density:
         if letter in density_list[i]:
            density_diff[i] += (abs(unknow_book_density[letter] - density_list[i][letter]))
      for num in range(len(density_diff)):
         density_diff[num] = round(density_diff[num], 5)
   min_dif = density_diff.index(min(density_diff))
   print(f"\nМожливі автори: {authors_list} "
         f"\nРізниця між функціями щільностей невідомого тексту і авторів: {density_diff}"
         f"\nАвтор невідомого тексту: {authors_list[min_dif]}")
   
   
main()
