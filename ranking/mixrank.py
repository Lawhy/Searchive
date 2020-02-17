import json
import math
import search
import collections
import readindex

docid_set = search.query_docid
query = search.preprotext

def read(file):
    with open(file,"r") as f:
        text_1 = f.read()
        text = json.loads(text_1)
        f.close()
    return text

def tfidf_score_cal(df,tf):
    if df != 0 and tf != 0:
        w = (1 + math.log(float(tf),10))*math.log(5000/float(df),10)
        return w
    else:
        return 0

def bm25_score_cal(detail,df,tf):
    k1 = 2
    b = 0.75
    len_doc = detail["total_document_length"]
    no_doc = detail["total_doc_number"]
    avg_doc = float(len_doc/no_doc)
    idf = math.log((no_doc-float(df)+0.5)/(float(df)+0.5),10)
    score = idf * float(tf*(k1+1))/float(tf+k1*(1-b+b*float(len_doc)/avg_doc))
    return score

def weight_score(bm25,tfidf):
    w1 = 0.3
    w2 = 0.7
    dict_final = []
    for docid in docid_set:
        score = w1 * tfidf[docid]+ w2 * bm25[docid]
        dict_final.append((docid,score))
    return dict_final

def rank(query):
    dict_tfidf = {}
    dict_bm25 = {}
    dict_final = []
    tfidf_score = 0
    bm25_score = 0
    for docid in docid_set:
        for term in query:
            dict_term = readindex.read_index(term,"abstract")
            dict_detail = readindex.read_index(term,"param")
            
            docid.replace('.','-')
            df = dict_term["df"]
            tf = dict_term[docid]['tf']
            
            tfidf_score = tfidf_score + tfidf_score_cal(df,tf)
            bm25_score = bm25_score + bm25_score_cal(dict_detail,df,tf)
        docid.replace('-','.')
        dict_tfidf[docid] = tfidf_score
        dict_bm25[docid] = bm25_score
        tfidf_score = 0
        bm25_score = 0
    dict_final = weight_score(dict_bm25,dict_tfidf)
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

def getResult(query):
    dict_final = rank(query)
    dict_final_w = sorted(dict_final, key = lambda x:x[1], reverse = True)
    dict_result = search_for_detail(dict_final_w)
    return dict_result

#{term:{docid1:{'pos':[],'tf':??},docid2:{},'df':??},term:{}}
#{term:{total_doc_number:??,total_doc_length:??},term:{}}