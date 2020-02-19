import math
import sys
import json
import collections

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
    w = 1 + math.log10(float(tf)) * math.log10(5000/float(df))
    return w

def rank(raw_query,query,mode):
    docid_set = mode_select(raw_query,mode)
    dict_term = {}
    if docid_set == "None":
        return "None"
    else:
        dict_tfidf = []
        # speed up
        for term in query:
            if read_index(term,mode) != None:
                dict_term[term] = read_index(term,mode)
        
        for docid in docid_set:
            tfidf_score = 0
            for term in dict_term.keys():
                # whether term exists in index
                df = dict_term[term]["df"]
                if docid in dict_term[term].keys():
                    tf = dict_term[term][docid]['tf']
                    tfidf_score += tfidf_score_cal(df,tf)
                else:
                    tfidf_score = tfidf_score
            dict_tfidf.append((docid,tfidf_score))
        dict_tfidf_sort = sorted(dict_tfidf, key = lambda x:x[1], reverse = True)
        return dict_tfidf_sort

# speed up
def cate(dict_final):
    dict_classi = collections.defaultdict(list)
    for each_list in dict_final:
        doc_id_f = each_list[0].replace('-','.')
        doc_id = int(float(doc_id_f))
        dict_classi[doc_id].append(doc_id_f)
    return dict_classi #{json name:[doci_id1,doc_id2,...]}

def search_for_detail(raw_query,mode="abstract"):
    query = preprocess_squery(raw_query,mode)
    # ordered list of tuples [(doc_id, score),()]
    dict_final = rank(raw_query,query,mode)
    dict_result = {}
    result_final_all = []
    if dict_final == 'None':
        return []
    else:
        dict_classi = cate(dict_final)
        # get all details of all doc_id but not in order
        for key in dict_classi.keys():
            filepath =  '../../data/' + str(key) + '.json'
            dict_1907 = read(filepath)
            for doc_id_temp in dict_classi[key]:
                dict_result[doc_id_temp] = dict_1907[doc_id_temp]
        # order the results
        for item in dict_final:
            doc_id_norm = item[0].replace('-','.')
            dict_result_temp = dict_result[doc_id_norm]
            dict_result_temp["id"] = doc_id_norm
            dict_result_temp['score'] = item[1]
            result_final_all.append(dict_result_temp)
        # limit the number of documents shown to users
        if len(result_final_all) > 1000:
            result_final_all = result_final_all[:1000]
        return result_final_all