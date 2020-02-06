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

def bm25_rank(filepath2,text):
    dict_weight = []
    detail = read(filepath2)
    score = 0
    for docid in docid_set:
        for term in query:
            df = text[term]["df"]
            tf = text[term]["docdict"][docid]["tf"]
            score = score + score_cal(docid,term,detail,df,tf)
        dict_weight.append((docid,score))
        score = 0
    return dict_weight

def score_cal(docid,term,detail,df,tf):
    k1 = 2
    b = 0.75
    idf = math.log((detail["sum_doc"]-float(df)+0.5)/(float(df)+0.5),10)
    len_doc = detail[docid]
    tf = text[term]["docdict"][docid]["tf"]
    score = idf * float(tf*(k1+1))/float(tf+k1*(1-b+b*float(len_doc)/float(detail["avg_doc"])))
    return score

def write(filepath,rank_dict):
    with open(filepath,"w") as f_wrindex:
         json.dump(rank_dict,f_wrindex)
    f_wrindex.close()
    
text = read(filepath)
bm25_dict = bm25_rank(filepath2,text)
write(filepath3,bm25_dict)

# bm25_dict = {"sum_doc":???,"doc_id 1":length,"doc_id 2": length}

# {word : {"df": xx, "docdict":{doc_id 1:{"tf": yy, "pos": [postlist]} , doc_id 2}}}
        