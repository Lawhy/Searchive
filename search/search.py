import json
import math
import re
from nltk.stem import *
from nltk.corpus import stopwords


def readindex(file_path):
    with open(file_path, "r") as f:
        text_t = f.read()
        text = json.loads(text_t)
        f.close()
    return text #type dict

'''preprocess search query'''
def preprocess_squery(query):
    #query = search_query
    tokenised_text = re.findall("\w+",query)  # split on all the non-letter words, keep the words consisting of numbers or/and letters
    lowered_text = [w.lower() for w in tokenised_text]  # case folding
    stopped_text = [word for word in lowered_text if word not in stopwords.words('english')]  # remove stop words
    stemmer = PorterStemmer()
    stemmed_text = [stemmer.stem(word) for word in stopped_text]  # stemming
    len_of_query = stemmed_text.__len__()
    return stemmed_text,len_of_query

def term_search(term):
    posi_list = []
    if readindex(file_path).__contains__(term):
        posi_list = list(text[term]['docdict'].keys())
    return posi_list

def search(query):
    len_of_query = preprocess_squery(query)[1]
    term = preprocess_squery(query)[0]
    i = 0
    query_list = []
    while i < len_of_query:
        query_list.append(term_search(term[i]))
        i += 1

    query_docid = set(query_list[0])
    for value in iter(query_list[1:]):
        query_docid = query_docid.union(value) #.intersection(value)

    return query_docid

# phrase search--2 terms
def phrase_search(search_phrase):
    len_of_query = preprocess_squery(search_phrase)[1]
    term = preprocess_squery(search_phrase)[0]
    t1 = set(term_search(term[0]))
    t2 = set(term_search(term[1]))
    term_ids = list(t1 & t2)

    i = 0
    IDs1 = readindex(file_path).get(term[0]).get('docdict')
    IDs2 = readindex(file_path).get(term[1]).get('docdict')
    print(IDs1)
    print(IDs2)
    IDt1t2 = []

    while i < term_ids.__len__():
        posi1 = IDs1.get(term_ids[i])['pos']
        posi2 = IDs2.get(term_ids[i])['pos']
        m = 0
        n = 0
        while m < posi1.__len__():
            while n < posi2.__len__():
                if (int(posi2[n]) - int(posi1[m]) == 1):
                    IDt1t2.append(term_ids[i])
                n += 1
            m += 1
        i += 1
    return IDt1t2


file_path = '/Users/mac/Downloads/index1901.json'
text = readindex(file_path)

search_query = "effective energy density"
preprotext = preprocess_squery(search_query)[0]
print(search(search_query))

search_phrase = "effective energy"
print(phrase_search(search_phrase))

# {word : {"df": xx, "docdict":{doc_id 1:{"tf": yy, "pos": [postlist]} , doc_id 2}}}

