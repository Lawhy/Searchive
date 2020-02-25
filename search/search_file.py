import json
import math
import re
import pickle
from nltk.stem import *
from nltk.corpus import stopwords
from time import *
import sys
sys.path.append('..')  # append the main directory path
from preprocess.normalise import Normaliser

'''index dict posonly--phrase search, index dict--query search.  index_no_pos and index_mongo_only_pos'''
abs_pos={}
aut_pos={}
tit_pos={}
abs={}
aut={}
tit={}
def read_index_file(filepath):
    """read the index back to the dictinoary"""
    with open(filepath, "rb") as f:
        text = f.read()
        dict = pickle.loads(text)
        f.close()
        return dict

'''preprocess search query'''
def preprocess_squery(query,mode):
    norm = Normaliser()
    if mode == 'author':
        clean_text = norm.normalise_author(query)
    else:
    # get tokens from the raw text
        clean_text = norm.normalise_text(query)

    return clean_text  #len_of_query


'''    term search   '''
def term_search(term,mode,dictindex):
    # mode = mode
    docid_list = []
    if dictindex.__contains__(term):
        term_dic = dictindex[term]
        docid = term_dic.keys()
        for item in docid:
            if item != 'df':  # and item!= '_id':
                docid_list.append(item)
        return docid_list
    else:
        return '0'


'''   query search   '''
def query_search(query,mode,dictindex):

    term = preprocess_squery(query, mode)
    len_of_query = term.__len__()
    i = 0
    query_list = []
    while i < len_of_query:
        if term_search(term[i],mode,dictindex) == '0':
            i += 1
        else:
            query_list.append(term_search(term[i],mode,dictindex))
            i += 1

    if query_list.__len__() > 0:
        query_docid = set(query_list[0])
        for value in iter(query_list[1:]):
            query_docid = query_docid.union(value)  # .intersection(value)
        if query_docid.__len__() == 0:
            return 'None'
        else:
            return query_docid
    else:
        return 'None'



# 'teitelboim', {'1901-00014': [97], '1901-00977': [3], '1901-04128': [5], '1901-08877': [8], '1801-10537': [3]}
'''    term search   '''
def term_psearch(term,mode,dictindex):
    mode = mode
    if dictindex.__contains__(term):
        term_dic = dictindex[term]
        docid_list = term_dic.keys()
        if len(docid_list) != 0:
            return docid_list
        else:
            return '0'
    else:
        return '0'

''' phrase search--n terms '''
def phrase_search(search_phrase,mode,dictindex):
    term = preprocess_squery(search_phrase,mode)
    len_of_query = term.__len__()

    t1 = set(term_psearch(term[0],mode,dictindex))
    t2 = set(term_psearch(term[-1],mode,dictindex))
    if t1 == set('0') or t2 == set('0'):
        return 'None'

    else:

        term_ids = list(t1 & t2)
        IDtftl = []  # doc_id contains the first and last word
        term_dic_f = dictindex[term[0]]
        term_dic_l = dictindex[term[-1]]

        for docid in term_ids:
            if term_dic_f.__contains__(docid) and term_dic_l.__contains__(docid):
                posif = term_dic_f[docid]
                posil = term_dic_l[docid]
                m = 0
                n = 0
                while m < posif.__len__():
                    while n < posil.__len__():
                        if (int(posil[n]) - int(posif[m]) == len_of_query-1):
                            IDtftl.append(docid)
                        n += 1
                    m += 1

        docid_phrase = []
        if len_of_query > 2:
            for id_query in IDtftl:
                for i in range(len_of_query-1):
                    dictf = dictindex[term[i]]
                    dictl = dictindex[term[i+1]]
                    if dictf.__contains__(id_query) and dictl.__contains__(id_query):
                        posif = dictf[id_query]
                        posil = dictl[id_query]
                        m = 0
                        n = 0
                        while m < posif.__len__():
                            while n < posil.__len__():
                                if (int(posil[n]) - int(posif[m]) == 1):
                                    docid_phrase.append(id_query)
                                n += 1
                            m += 1
        else:
            docid_phrase = IDtftl

        phrase_docid = set(docid_phrase)
        if docid_phrase.__len__() == 0:
            return 'None'
        else:
            return phrase_docid

def mode_select(query,mode,abs,tit,aut,abs_pos,tit_pos,aut_pos):
    begin_time = time()
    query_docid = None

    if mode == 'general':
        if query[0]=='\"' and query[-1] == '\"':
            query_docid_abs = phrase_search(query, 'abstract',abs_pos)
            query_docid_title = phrase_search(query, 'title',tit_pos)
            query_docid_author = phrase_search(query, 'author',aut_pos)
        else:
            query_docid_abs = query_search(query,'abstract',abs)
            query_docid_title = query_search(query, 'title',tit)
            query_docid_author = query_search(query, 'author',aut)

        if query_docid_abs != 'None' and query_docid_title != 'None' and query_docid_author != 'None':
            query_docid = query_docid_abs.union(query_docid_title, query_docid_author)
        elif query_docid_abs == 'None' and query_docid_title != 'None' and query_docid_author != 'None':
            query_docid = query_docid_title.union(query_docid_author)
        elif query_docid_abs != 'None' and query_docid_title == 'None' and query_docid_author != 'None':
            query_docid = query_docid_abs.union(query_docid_author)
        elif query_docid_abs != 'None' and query_docid_title != 'None' and query_docid_author == 'None':
            query_docid = query_docid_title.union(query_docid_abs)
        elif query_docid_abs != 'None' and query_docid_title == 'None' and query_docid_author == 'None':
            query_docid = query_docid_abs
        elif query_docid_abs == 'None' and query_docid_title != 'None' and query_docid_author == 'None':
            query_docid = query_docid_title
        elif query_docid_abs == 'None' and query_docid_title == 'None' and query_docid_author != 'None':
            query_docid = query_docid_author

    else: #mode abs tit aut
        if mode == 'abstract':
            if query[0] == '\"' and query[-1] == '\"': # phrase search
                dictindex = abs_pos
                query_docid = phrase_search(query, mode, dictindex)
            else:                                      # query search
                dictindex = abs
                query_docid = query_search(query, mode, dictindex)
        elif mode == 'title':
            if query[0] == '\"' and query[-1] == '\"': # phrase search
                dictindex = tit_pos
                query_docid = phrase_search(query, mode, dictindex)
            else:                                      # query search
                dictindex = tit
                query_docid = query_search(query, mode, dictindex)
        elif mode == 'author':
            if query[0] == '\"' and query[-1] == '\"': # phrase search
                dictindex = aut_pos
                query_docid = phrase_search(query, mode, dictindex)
            else:                                      # query search
                dictindex = aut
                query_docid = query_search(query, mode, dictindex)

    end_time = time()
    run_time = end_time - begin_time
    print('search time', run_time)
    return query_docid

def readindexfile():
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
    print('load time', time_end - time_start)
    return
# time_start = time()
# filepath_abs = '../data/abs_dict'
# abs = read_index_file(filepath_abs)
# filepath_tit = '../data/title_dict'
# tit = read_index_file(filepath_tit)
# filepath_aut = '../data/author_dict'
# aut = read_index_file(filepath_aut)
#
# filepath_abs_pos = '../data/abs_pos.pkl'
# abs_pos = read_index_file(filepath_abs_pos)
# filepath_aut_pos = '../data/author_pos.pkl'
# aut_pos = read_index_file(filepath_aut_pos)
# filepath_tit_pos = '../data/title_pos.pkl'
# tit_pos = read_index_file(filepath_tit_pos)
#
# time_end = time()
# print('load time', time_end-time_start)


if __name__ == '__main__':
    '''test'''
    search_query = "constant spacetime mean curvature surfaces"
    mode = 'general'  #mode = 'abstract' / 'title' / 'author'/ 'param'
    search_phrase = "\"obtained results\""
    print(mode_select(search_query,'general',abs,tit,aut,abs_pos,aut_pos,tit_pos).__len__())
    print(mode_select(search_phrase,'general',abs,tit,aut,abs_pos,aut_pos,tit_pos))