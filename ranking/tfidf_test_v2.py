import math
import sys
import json
import time

sys.path.append('..')  # append the main directory path
from search.search import mode_select, preprocess_squery
from indexing.readindex import read_index

def read(filepath):
    with open(filepath,'r') as f:
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

def rank(raw_query,query,mode):
    docid_set = mode_select(raw_query,mode)
    if docid_set == "None":
        return "None"
    else:
        dict_tfidf = []
        tfidf_score = 0
        start_time5 = time.time()
        for docid in docid_set:
            for term in query:
                if read_index(term,mode) != None:
                    dict_term = read_index(term, mode)
                    df = dict_term["df"]
                    if docid in dict_term.keys():
                        tf = dict_term[docid]['tf']
                    else:
                        tf = 0
                else:
                    df = 0
                    tf = 0
                tfidf_score = tfidf_score + tfidf_score_cal(df, tf)
            dict_tfidf.append((docid,tfidf_score))
            tfidf_score = 0
        dict_tfidf_sort = sorted(dict_tfidf, key = lambda x:x[1], reverse = True)
        print("--- for loop: %s seconds ---" % (time.time() - start_time5))
        return dict_tfidf_sort

def search_for_detail(raw_query,mode="abstract"):
    start_time1 = time.time()
    query = preprocess_squery(raw_query,mode)
    print("--- preprocess the query: %s seconds ---" % (time.time() - start_time1))
    start_time2 = time.time()
    dict_final = rank(raw_query,query,mode)
    print("--- ranking process: %s seconds ---" % (time.time() - start_time2))
    
    if dict_final == 'None':
        return []
    else:
        result_list = []
        start_time3 = time.time()
        for each_list in dict_final:
            dict_result_temp = {}
            doc_id_p = each_list[0].replace('-','.')
            doc_id = int(float(doc_id_p))
            filepath = '../../data/' + str(doc_id) + '.json'
            dict_1907 = read(filepath)
            dict_result_temp = dict_1907[doc_id_p]
            dict_result_temp["id"] = doc_id_p
            dict_result_temp['score'] = each_list[1]
            result_list.append(dict_result_temp)
        print("--- search for detail: %s seconds ---" % (time.time() - start_time3))
        return result_list
