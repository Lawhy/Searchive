import sys
sys.path.append('..')  # append the main directory path
import pickle
from time import *
from search_file import mode_select
def read_index_file(filepath):
    """read the index back to the dictinoary"""
    with open(filepath, "rb") as f:
        text = f.read()
        dict = pickle.loads(text)
        f.close()
        return dict

time_start = time()
filepath_abs = '../data/abs_dict'
abs = read_index_file(filepath_abs)
filepath_tit = '../data/title_dict'
tit = read_index_file(filepath_tit)
filepath_aut = '../data/author_dict'
aut = read_index_file(filepath_aut)

filepath_abs_pos = '../data/abs_pos.pkl'
abs_pos = read_index_file(filepath_abs_pos)
filepath_aut_pos = '../data/author_pos.pkl'
aut_pos = read_index_file(filepath_aut_pos)
filepath_tit_pos = '../data/title_pos.pkl'
tit_pos = read_index_file(filepath_tit_pos)

time_end = time()
print('load time', time_end-time_start)
search_query = "constant spacetime mean curvature surfaces"
mode = 'general'  #mode = 'abstract' / 'title' / 'author'/ 'param'
search_phrase = "\"obtained results\""
print(mode_select(search_query,'general',abs,tit,aut,abs_pos,aut_pos,tit_pos).__len__())
print(mode_select(search_phrase,'general',abs,tit,aut,abs_pos,aut_pos,tit_pos))

