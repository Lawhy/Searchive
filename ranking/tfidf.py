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
    
def score_cal(df,tf):
    if df != 0 and tf != 0:
        w = (1 + math.log(float(tf),10))*math.log(5000/float(df),10)
        return w
    else:
        return 0
    
def rank(filepath_query,json_text):
    query_stem = get_query(filepath_query)
    rank_dict = {}
    text = json.loads(json_text)
    total_score = 0
    query_no = 1000
    for word in query_stem:
        if word in text.keys():
            df = text[word]["df"]
            score = 0
            for keys in text[word]["docdict"].keys():
                tf = text[word]["docdict"][keys]["tf"]
                score += score_cal(df,tf)
        total_score += score
    print("query: %f total_score: %f" % query_no, total_score)
    rank_dict[query_no] = total_score

def write(filepath,rank_dict):
    with open(filepath,"w") as f_wrindex:
         json.dump(rank_dict,f_wrindex)
    f_wrindex.close()

query = get_query(filepath_query)
start_time = time.time()
text = read(filepath)
rank_dict = rank(text)
write(filepath,rank_dict)
print("--- %s seconds ---" % (time.time() - start_time))

# {word : {"df": xx, "docdict":{doc_id 1:{"tf": yy, "pos": [postlist]} , doc_id 2}}}