import math
import sys
import json
import collections

sys.path.append('..')  # append the main directory path
from search.search_mongo_file import mode_select, preprocess_squery
from indexing.index_no_pos import read_index_file

ab = read_index_file("../../data/abs_dict")
au = read_index_file("../../data/author_dict")
ti = read_index_file("../../data/title_dict")

def read(filepath):
    with open(filepath,'r') as f:
        text_1 = f.read()
        text = json.loads(text_1)
        f.close()
    return text

def tfidf_score_cal(df,tf):
    w = 1 + math.log10(float(tf)) * math.log10(5000/float(df))
    return w

def bm25_score_cal(dict_param,df,tf,mode):
    k1 = 2
    b = 0.75
    no_doc = dict_param["dno"]
    if mode == "abstract":
        len_doc = dict_param["abl"]
    elif mode == "authors":
        len_doc = dict_param["aul"]
    elif mode == "title":
        len_doc = dict_param["til"]

    avg_doc = float(len_doc/no_doc)
    idf = math.log((no_doc-float(df)+0.5)/(float(df)+0.5),10)
    score = idf * float(tf*(k1+1))/float(tf+k1*(1-b+b*float(len_doc)/avg_doc))
    return score

def weight_score(bm25,tfidf):
    w1 = 0.3
    w2 = 0.7
    dict_mix = []
    for docid in bm25:
        score = w1 * tfidf[docid]+ w2 * bm25[docid]
        dict_mix.append((docid,score))
    dict_mix_sort = sorted(dict_mix, key=lambda x: x[1], reverse=True)
    return dict_mix_sort

def tfidf(docid_set,dict_term,mix):
    dict_tfidf = []
    for docid in docid_set:
        tfidf_score = 0
        for term in dict_term.keys():
            # whether term exists in index
            df = dict_term[term]["df"]
            if docid in dict_term[term].keys():
                tf = dict_term[term][docid]
                tfidf_score += tfidf_score_cal(df, tf)
            else:
                tfidf_score = tfidf_score
        dict_tfidf.append((docid, tfidf_score))
    if mix:
        return dict_tfidf
    else:
        dict_tfidf_sort = sorted(dict_tfidf, key=lambda x: x[1], reverse=True)
        return dict_tfidf_sort

# mix = True : no sort before add to speed up.
#       False : sort directly
def bm25(docid_set,dict_term,mode,mix):
    dict_param = read_index_file("../../data/param_dict")
    dict_bm25 = []
    for docid in docid_set:
        bm25_score = 0
        for term in dict_term.keys():
            df = dict_term[term]["df"]
            if docid in dict_term[term].keys():
                tf = dict_term[term][docid]
                bm25_score = bm25_score + bm25_score_cal(dict_param,df,tf,mode)
            else:
                bm25_score = bm25_score
        dict_bm25.append((docid,bm25_score))
    if mix:
        return dict_bm25
    else:
        dict_bm25_sort = sorted(dict_bm25, key=lambda x: x[1], reverse=True)
        return dict_bm25_sort

def mix(docid_set,dict_term,mode):
    tfidf_result = dict(tfidf(docid_set,dict_term,True))
    bm25_result = dict(bm25(docid_set,dict_term,mode,True))
    return weight_score(bm25_result,tfidf_result)

def rank(raw_query,query,mode,dictindex,method):
    docid_set = mode_select(raw_query,mode,ab,ti,au)
    dict_term = {}

    if docid_set == "None":
        return "None"
    else:
        # speed up
        for term in query:
            if dictindex[term] != None:
                dict_term[term] = dictindex[term]

        if method == 'tfidf':
            return tfidf(docid_set,dict_term,False)
        elif method == 'bm25':
            return bm25(docid_set,dict_term,mode,False)
        elif method == 'mix':
            return mix(docid_set,dict_term,mode)

# speed up
def cate(dict_final):
    dict_classi = collections.defaultdict(list)
    for each_list in dict_final:
        doc_id_f = each_list[0].replace('-','.')
        doc_id = int(float(doc_id_f))
        dict_classi[doc_id].append(doc_id_f)
    return dict_classi #{json name:[doci_id1,doc_id2,...]}

# method = 'tfidf'
#          'bm25'
#          'mix'
def search_for_detail(raw_query,mode="abstract",method = 'mix'):
    query = preprocess_squery(raw_query,mode)
    # ordered list of tuples [(doc_id, score),()]
    if mode == 'abstract':
        dict_final = rank(raw_query,query,mode,ab,method)
    elif mode == 'author':
        dict_final = rank(raw_query,query,mode,au,method)
    elif mode == 'title':
        dict_final = rank(raw_query,query,mode,ti,method)
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