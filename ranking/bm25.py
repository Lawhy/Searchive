import json
import math
import search

docid_set = search.query_docid
query = search.preprotext

def read(file):
    with open(file,"r") as f:
        text_1 = f.read()
        text = json.loads(text_1)
        f.close()
    return text

def bm25_rank(bm25,text):
    dict_weight = []
    detail = bm25
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

#def write(filepath,rank_dict):
#    with open(filepath,"w") as f_wrindex:
#         json.dump(rank_dict,f_wrindex)
#    f_wrindex.close()
    
text = read('/afs/inf.ed.ac.uk/user/s19/s1926829/TTDS/test/index1901.json')
bm25 = read('/afs/inf.ed.ac.uk/user/s19/s1926829/TTDS/test/index25.json')
bm25_dict = bm25_rank(bm25,text)
bm25_dict_w = sorted(bm25_dict,key = lambda x:x[1], reverse = True)
print(bm25_dict_w)

# bm25_dict = {"sum_doc":???,"doc_id 1":length,"doc_id 2": length}

# {word : {"df": xx, "docdict":{doc_id 1:{"tf": yy, "pos": [postlist]} , doc_id 2}}}
        