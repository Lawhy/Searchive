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
        query_docid = query_docid.intersection(value)

    return query_docid

file_path = '/Users/mac/Downloads/index1901.json'
text = readindex(file_path)
search_query = "effective energy density"
print(search(search_query))


# {word : {"df": xx, "docdict":{doc_id 1:{"tf": yy, "pos": [postlist]} , doc_id 2}}}

