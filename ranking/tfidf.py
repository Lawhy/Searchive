import json
import math
import search

docid_set = search.query_docid
query = search.preprotext

def read(file):
    with open(filepath,"r") as f:
        text = f.read()
        f.close()
    return text

def rank(query_word,text):
    dict_weight = []
    score = 0
    for docid in docid_set:
        for term in query_word:
            df = text[term]["df"]
            tf = text[term]["docdict"][docid]["tf"]
            score = score + score_cal(df,tf)
        dict_weight.append((docid,score))
        score = 0
    return dict_weight
    
def score_cal(df,tf):
    if df != 0 and tf != 0:
        w = (1 + math.log(float(tf),10))*math.log(5000/float(df),10)
        return w
    else:
        return 0

def write(filepath,rank_dict):
    with open(filepath,"w") as f_wrindex:
         json.dump(rank_dict,f_wrindex)
    f_wrindex.close()

text = read(filepath)
dict_w = rank(query,text)
dict_w_sort = sorted(dict_w,key = lambda x:x[1], reverse = True)
write(filepath2,dict_w_sort)
# {word : {"df": xx, "docdict":{doc_id 1:{"tf": yy, "pos": [postlist]} , doc_id 2}}}