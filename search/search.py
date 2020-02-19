import json
import math
import re
from nltk.stem import *
from nltk.corpus import stopwords

import sys
sys.path.append('..')  # append the main directory path
from preprocess.normalise import Normaliser
from indexing.readindex import read_index
# from readindex import read_index
# from normalise import Normaliser

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
def term_search(term,mode):
    # posi_list = []
    # if readindex(file_path).__contains__(term):
    #     posi_list = list(text[term]['docdict'].keys())
    # return posi_list
    docid_list = []

    term_dic = read_index(term,mode)
    if term_dic == None: #term is not in index
        return '0'

    else :
        docid = term_dic.keys()
        for item in docid:
            if item != 'df':
                docid_list.append(item)
        return docid_list

'''   query search   '''
def query_search(query,mode):

    term = preprocess_squery(query, mode)
    len_of_query = term.__len__()
    i = 0
    query_list = []
    while i < len_of_query:
        if term_search(term[i] , mode) == '0':
            i += 1
        else:
            query_list.append(term_search(term[i],mode))
            i += 1
    #print(query_list.__len__())
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


''' phrase search--n terms '''
def phrase_search(search_phrase,mode):
    # len_of_query = preprocess_squery(search_phrase,mode)[1]
    term = preprocess_squery(search_phrase,mode)
    len_of_query = term.__len__()

    t1 = set(term_search(term[0],mode))
    t2 = set(term_search(term[-1],mode))
    term_ids = list(t1 & t2)

    i = 0
    # {'1901-00001': {'pos': [59], 'tf': 1}, 'df': 1}
    IDtftl = [] # doc_id contains the first and last word

    term_dic_f = read_index(term[0], mode)
    term_dic_l = read_index(term[-1], mode)

    for docid in term_ids:
        posif = term_dic_f.get(docid)['pos']
        posil = term_dic_l.get(docid)['pos']
        m = 0
        n = 0
        while m < posif.__len__():
            while n < posil.__len__():
                if (int(posil[n]) - int(posif[m]) == len_of_query-1):
                    IDtftl.append(term_ids[i])
                n += 1
            m += 1
    docid_phrase = []
    if len_of_query > 2:
        for id_query in IDtftl:
            i = 1
            while i < len_of_query - 1:
                posif = read_index(term[i-1], mode).get(id_query)['pos']
                posil = read_index(term[i], mode).get(id_query)['pos']
                m = 0
                n = 0
                while m < posif.__len__():
                    while n < posil.__len__():
                        if (int(posil[n]) - int(posif[m]) != 1):
                            break
                        else:
                            docid_phrase.append(id_query)
                        n += 1
                    m += 1
                i += 1
    else:
        docid_phrase = IDtftl
    query_docid = set(docid_phrase)

    if query_docid.__len__() == 0:
        return 'None'
    else:
        return query_docid
    # return query_docid

def mode_select(query,mode):
    if mode == 'general':
        if query[0]=='\"' and query[-1] == '\"':
            query_docid_abs = phrase_search(query, 'abstract')
            query_docid_title = phrase_search(query, 'title')
            query_docid_author = phrase_search(query, 'author')
        else:
            query_docid_abs = query_search(query,'abstract')
            query_docid_title = query_search(query, 'title')
            query_docid_author = query_search(query, 'author')
        query_docid = query_docid_abs.union(query_docid_title , query_docid_author)
    else:
        if query[0]=='\"' and query[-1] == '\"':
            query_docid = phrase_search(query, mode)
        else:
            query_docid = query_search(query,mode)
    return query_docid



#
# '''test'''
# search_query = "effective energy density"
# mode = 'general'  #mode = 'abstract' / 'title' / 'author'/ 'param'
# search_phrase = "\"computer science\""
# search_query= "science"
#
# print(mode_select(search_phrase,mode))
# print(mode_select(search_query,'abstract'))