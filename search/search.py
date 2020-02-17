import json
import math
import re
from nltk.stem import *
from nltk.corpus import stopwords

import sys
import readindex
sys.path.append('..')  # append the main directory path
from preprocess.normalise import Normaliser
# from normalise import Normaliser

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
    len_of_query = clean_text.__len__()
    return clean_text,len_of_query

def term_search(term,mode):
    # posi_list = []
    # if readindex(file_path).__contains__(term):
    #     posi_list = list(text[term]['docdict'].keys())
    # {word : {"df": xx, "docdict":{doc_id 1:{"tf": yy, "pos": [postlist]} , doc_id 2}}}
    # return posi_list
    docid_list = []
    term_dic = readindex.read_index(term,mode)
    docid = term_dic.keys()
    for item in docid:
        if item != 'df':
            docid_list.append(item)
    return docid_list

def query_search(query,mode):
    len_of_query = preprocess_squery(query,mode)[1]
    term = preprocess_squery(query,mode)[0]
    i = 0
    query_list = []
    while i < len_of_query:
        query_list.append(term_search(term[i],mode))
        i += 1
    query_docid = set(query_list[0])
    for value in iter(query_list[1:]):
        query_docid = query_docid.union(value) #.intersection(value)
    return query_docid

# phrase search--n terms
def phrase_search(search_phrase,mode):
    len_of_query = preprocess_squery(search_phrase,mode)[1]
    term = preprocess_squery(search_phrase,mode)[0]
    t1 = set(term_search(term[0],mode))
    t2 = set(term_search(term[-1],mode))
    term_ids = list(t1 & t2)
    i = 0
    # {'1901-00001': {'pos': [59], 'tf': 1}, 'df': 1}
    # {word: {"df": xx, "docdict": {doc_id 1: {"tf": yy, "pos": [postlist]}, doc_id 2}}}

    IDtftl = [] # doc_id contains the first and last word

    term_dic_f = readindex.read_index(term[0], mode)
    term_dic_l = readindex.read_index(term[-1], mode)

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

    # docid_phrase = []
    # if len_of_query > 2:
    #     for docid in IDtftl:
    #         posif = term_dic_f.get(docid)['pos']
    #         posil = readindex.read_index(term[1], mode).get(docid)['pos']

    return IDtftl

search_query = "effective energy density"
mode = 'abstract'
# mode = 'abstract' / 'title' / 'author'/ 'param'
# print(term_search('effect',mode))

preprotext = preprocess_squery(search_query,mode)[0]
query_docid = query_search(search_query,mode)
# print(query_docid)

search_phrase = "subsequent decline despite"
# print(phrase_search(search_phrase,mode))


