import json
import math
import search
import collections

docid_set = search.query_docid
query = search.preprotext

def read(file):
    with open(file,"r") as f:
        text_1 = f.read()
        text = json.loads(text_1)
        f.close()
    return text

def tfidf_rank(query_word,text):
    dict_weight = {}
    score = 0
    for docid in docid_set:
        for term in query_word:
            df = text[term]["df"]
            tf = text[term]["docdict"][docid]["tf"]
            score = score + tfidf_score_cal(df,tf)      
        dict_weight[docid] = score
        score = 0
    return dict_weight
    
def tfidf_score_cal(df,tf):
    if df != 0 and tf != 0:
        w = (1 + math.log(float(tf),10))*math.log(5000/float(df),10)
        return w
    else:
        return 0

def bm25_rank(bm25,text):
    dict_weight = {}
    detail = bm25
    score = 0
    for docid in docid_set:
        for term in query:
            df = text[term]["df"]
            tf = text[term]["docdict"][docid]["tf"]
            score = score + bm25_score_cal(docid,term,detail,df,tf)
        dict_weight[docid] = score
        score = 0
    return dict_weight

def bm25_score_cal(docid,term,detail,df,tf):
    k1 = 2
    b = 0.75
    idf = math.log((detail["sum_doc"]-float(df)+0.5)/(float(df)+0.5),10)
    len_doc = detail[docid]
    tf = text[term]["docdict"][docid]["tf"]
    score = idf * float(tf*(k1+1))/float(tf+k1*(1-b+b*float(len_doc)/float(detail["avg_doc"])))
    return score

def weight_score(bm25,tfidf):
    w1 = 0.3
    w2 = 0.7
    dict_final = []
    for docid in docid_set:
        score = w1 * tfidf[docid]+ w2 * bm25[docid]
        dict_final.append((docid,score))
    return dict_final

def search_for_detail(dict_w_sort):
    dict_result = collections.OrderedDict()
    for each_list in dict_w_sort:
        doc_id = int(float(each_list[0]))
        filepath = '/afs/inf.ed.ac.uk/user/s19/s1926829/TTDS/test/' + str(doc_id) + '.json'
        dict_1901 = read(filepath)
        dict_result[each_list[0]] = dict_1901[each_list[0]]
        dict_result[each_list[0]]['score'] = each_list[1]
    return dict_result
  
def write(filepath,rank_dict):
    with open(filepath,"w") as f_wrindex:
         json.dump(rank_dict,f_wrindex)
    f_wrindex.close()

text = read('/afs/inf.ed.ac.uk/user/s19/s1926829/TTDS/test/index1901.json')
bm25 = read('/afs/inf.ed.ac.uk/user/s19/s1926829/TTDS/test/index25.json')

dict_w = tfidf_rank(query,text)

bm25_dict = bm25_rank(bm25,text)

dict_final = weight_score(bm25_dict,dict_w)
dict_final_w = sorted(dict_final, key = lambda x:x[1], reverse = True)

dict_result = search_for_detail(dict_final_w)
write('/afs/inf.ed.ac.uk/user/s19/s1926829/TTDS/test/rank_tfidf_1901_detail.json',dict_result)
# {word : {"df": xx, "docdict":{doc_id 1:{"tf": yy, "pos": [postlist]} , doc_id 2}}}