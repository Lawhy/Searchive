import json
import math
import re
from nltk.stem import *
from nltk.corpus import stopwords
from time import *
import sys
sys.path.append('..')  # append the main directory path
from preprocess.normalise import Normaliser
from indexing.readindex_mongo import read_index
from indexing.index_no_pos import read_index_file
'''mongodb--ttds_pos--phrase search, index dict--query search.  index_no_pos and index_mongo_only_pos'''

dictindex_abs = {}
dictindex_tit = {}
dictindex_aut = {}

'''      read json file      '''
def readfile(file_path):
    with open(file_path, "r") as f:
        text_t = f.read()
        text = json.loads(text_t)
        f.close()
    return text #type dict

'''preprocess search query'''
def preprocess_squery(query,mode):
    # tokenised_text = re.findall("\w+",query)  # split on all the non-letter words, keep the words consisting of numbers or/and letters
    # lowered_text = [w.lower() for w in tokenised_text]  # case folding
    # stopped_text = [word for word in lowered_text if word not in stopwords.words('english')]  # remove stop words
    # stemmer = PorterStemmer()
    # clean_text = [stemmer.stem(word) for word in stopped_text]  # stemming
    norm = Normaliser()
    if mode == 'author':
        clean_text = norm.normalise_author(query)
    else:
    # get tokens from the raw text
        clean_text = norm.normalise_text(query)

    return clean_text  #len_of_query

'''    term search   '''
def term_search(term,mode,dictindex):
    docid_list = []
    term_dic = dictindex.get(term)

    if term_dic == None: #term is not in index
        return '0'
    else :
        docid = term_dic.keys()
        for item in docid:
            if item != 'df' and item!= '_id':
                docid_list.append(item)
        return docid_list

'''   query search   '''
def query_search(query,mode,dictindex):
    if mode == 'abstract':
        dictindex = dictindex_abs
    elif mode == 'title':
        dictindex = dictindex_tit
    elif mode == 'author':
        dictindex = dictindex_aut

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

'''    term search   '''
def term_psearch(term,mode):
    docid_list = []
    term_dic = read_index(term,mode)

    if term_dic == None or len(term_dic) == 1: #term is not in index
        return '0'
    else :
        docid = term_dic.keys()
        for item in docid:
            if item!= '_id':
                docid_list.append(item)
        return docid_list

''' phrase search--n terms '''
def phrase_search(search_phrase,mode):
    term = preprocess_squery(search_phrase,mode)
    len_of_query = term.__len__()

    t1 = set(term_psearch(term[0],mode))
    t2 = set(term_psearch(term[-1],mode))
    term_ids = list(t1 & t2)
    IDtftl = []  # doc_id contains the first and last word
    term_dic_f = read_index(term[0], mode)
    term_dic_l = read_index(term[-1], mode)

    i = 0
    if term_dic_f == None or term_dic_l == None:
        return 'None'
    else:
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
                dictf = read_index(term[i], mode)
                dictl = read_index(term[i+1], mode)
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

def mode_select(query,mode):
    begin_time = time()
    query_docid = None

    if mode == 'general':
        if query[0]=='\"' and query[-1] == '\"':
            query_docid_abs = phrase_search(query, 'abstract')
            query_docid_title = phrase_search(query, 'title')
            query_docid_author = phrase_search(query, 'author')
        else:
            query_docid_abs = query_search(query,'abstract',dictindex_abs)
            query_docid_title = query_search(query, 'title',dictindex_tit)
            query_docid_author = query_search(query, 'author',dictindex_aut)

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

    else:
        if query[0]=='\"' and query[-1] == '\"':
            query_docid = phrase_search(query, mode)
        else:
            if mode == 'abstract':
                # dictindex = dictindex_abs
                query_docid = query_search(query, mode, dictindex_abs)
            elif mode == 'title':
                # dictindex = dictindex_tit
                query_docid = query_search(query, mode, dictindex_tit)
            elif mode == 'author':
                # dictindex = dictindex_aut
                query_docid = query_search(query, mode, dictindex_aut)
            # query_docid = query_search(query,mode,dictindex)
    end_time = time()
    run_time = end_time - begin_time
    print('search time', run_time)
    return query_docid
#
# def read_index_dict():
#     time_start = time()
#     filepath_abs = '../data/abs_dict'
#     dictindex_abs = read_index_file(filepath_abs)
#     filepath_tit = '../data/title_dict'
#     dictindex_tit = read_index_file(filepath_tit)
#     filepath_aut = '../data/author_dict'
#     dictindex_aut = read_index_file(filepath_aut)
#     time_end = time()
#     print('load time', time_end - time_start)
#     return

# time_start = time()
filepath_abs = '../data/abs_dict'
dictindex_abs = read_index_file(filepath_abs)
filepath_tit = '../data/title_dict'
dictindex_tit = read_index_file(filepath_tit)
filepath_aut = '../data/author_dict'
dictindex_aut = read_index_file(filepath_aut)
# time_end = time()
# print('load time', time_end-time_start)

if __name__ == '__main__':
    '''test'''
    search_query = "constant spacetime mean curvature surfaces"
    mode = 'general'  #mode = 'abstract' / 'title' / 'author'/ 'param'
    search_phrase = "\"constant spacetime mean curvature surfaces\""
    print(mode_select(search_query,'abstract').__len__()) # result:search time 0.0037  # 13572
    print(mode_select(search_phrase,'general')) # result:search time 0.08  #1