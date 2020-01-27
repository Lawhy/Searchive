import json
import math
import time
import re

from nltk.stem import *
from nltk.corpus import stopwords

def read(file):
    with open(filepath,"r") as f:
        text = f.read()
        f.close()
    return text

def get_query(filepath_query):
    query = read(filepath_query)
    """ preprocessing """
    tokenised_text = re.findall("\w+",query)  # split on all the non-letter words, keep the words consisting of numbers or/and letters
    lowered_text = [w.lower() for w in tokenised_text]  # case folding
    stopped_text = [word for word in lowered_text if word not in stopwords]  # remove stop words
    stemmer = PorterStemmer()
    stemmed_text = [stemmer.stem(word) for word in stopped_text]  # stemming
    return stemmed_text

def bm25_rank(filepath_query, json_text):
    k1 = 2
    b = 0.75
    bm25_dict = {}
    detail = read(filepath2)
    text = json.loads(json_text)
    avg_docs = detail["avg_doc"]
    query_no = 1000
    query = get_query(filepath_query)
    total_score = 0
    for word in query:
        if word in text.keys():
            df = text[word]["df"]
            idf = math.log((detail["sum_doc"]-float(df)+0.5)/(float(df)+0.5),10)
            score = 0
            for keys in text[word]["docdict"].keys():
                len_doc = detail[keys]
                tf = text[word]["docdict"][keys]["tf"]
                score += float(tf*(k1+1))/float(tf+k1*(1-b+b*float(len_doc)/float(avg_docs)))
        total_score = idf*score
    print("query: %f total_score: %f" % query_no, total_score)
    bm25_dict[query_no] = total_score

def write(filepath,rank_dict):
    with open(filepath,"w") as f_wrindex:
         json.dump(rank_dict,f_wrindex)
    f_wrindex.close()
    
start_time = time.time()
text = read(filepath)
bm25_dict = bm25_rank(text)
write(filepath3,rank_dict)
print("--- %s seconds ---" % (time.time() - start_time))

# bm25_dict = {"sum_doc":???,"doc_id 1":length,"doc_id 2": length}

# {word : {"df": xx, "docdict":{doc_id 1:{"tf": yy, "pos": [postlist]} , doc_id 2}}}
        