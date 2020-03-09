import json
import time
import pickle
import sys
sys.path.append('..')
from preprocess.normalise import Normaliser

abs_dict = {}
title_dict = {}
author_dict = {}
param_dict = {'dno':0, #number of document
              'til':0, #total title length
              'abl':0, #total abstract length
              'aul':0} # total author length


def read(filepath):
    with open(filepath, "r") as f:
        json_text = f.read()
        text = json.loads(json_text)
        f.close()
    return text

"""structure {word:{"df":xx, doc_id : tf}}"""

def init_index(doc_id, text, dict):

    word_cnt = 0
    for word in text:
        word_cnt = word_cnt + 1
        if word not in dict:
            """first time"""
            dict[word]={}
            dict[word]["df"] = 1
            dict[word][doc_id]= 1
        else:
            dict[word]["df"] = dict[word]["df"] + 1
            if doc_id not in dict[word]:
                """first document"""
                dict[word][doc_id]= 1 # doc_id : tf , value is tf
            else:
                dict[word][doc_id] = dict[word][doc_id] + 1
    return word_cnt


def delete_word_index(dict, old_text, doc_id):
    for word in old_text:
        if word in dict.keys():
            if doc_id in dict[word].keys():
                tf_decre = dict[word][doc_id]
                dict[word]["df"] = dict[word]["df"] - tf_decre
                dict[word].pop(doc_id,None)
                if dict[word]["df"] == 0:
                    dict.pop(word,None)
    return


def initialise(filename):
    """
  Initialise index
  index start from 0
  """

    normaliser = Normaliser()

    doc_total = 0
    total_title_word = 0
    total_abs_word = 0
    total_author_word = 0

    text = read(filename)


    for key in text.keys():


        doc_total = doc_total + 1
        doc_id = key.replace(".", "-")
        print(doc_id)

        abstract = normaliser.normalise_text(text[key]["abs"])
        title = normaliser.normalise_text(text[key]["title"])
        author = normaliser.normalise_authors(text[key]["authors"])
        subjs = list(text[key]["subjs"].values())
        for sub in subjs:
            sub = normaliser.normalise_text(sub)
            abstract.extend(sub)

        """creating index"""
        file_title_cnt = init_index(doc_id, title, title_dict)
        file_abs_cnt = init_index(doc_id, abstract, abs_dict)
        file_author_cnt = init_index(doc_id, author, author_dict)
        total_abs_word = total_abs_word + file_abs_cnt
        total_title_word = total_title_word + file_title_cnt
        total_author_word = total_author_word + file_author_cnt


    param_dict['dno'] =  param_dict['dno'] + doc_total
    param_dict['abl'] = param_dict['abl'] + total_abs_word
    param_dict['til'] = param_dict['til'] + total_title_word
    param_dict['aul'] = param_dict['aul'] + total_author_word


    print("--- %s seconds ---" % (time.time() - start_time))
    return



def update(oldfile, newfile):

    normaliser = Normaliser()

    old_text = read(oldfile)
    new_text = read(newfile)

    title_len_diff_sum = 0
    abs_len_diff_sum = 0
    author_len_diff_sum = 0

    for key in old_text.keys():
        """every single docuement"""
        doc_id = key.replace(".", "-")
        print(doc_id)
        old_abstract = normaliser.normalise_text(old_text[key]["abs"])
        old_title = normaliser.normalise_text(old_text[key]["title"])
        old_author = normaliser.normalise_authors(old_text[key]["authors"])
        old_subjs = list(old_text[key]["subjs"].values())
        for sub in old_subjs:
            sub = normaliser.normalise_text(sub)
            old_abstract.extend(sub)

        new_abstract = normaliser.normalise_text(new_text[key]["abs"])
        new_title = normaliser.normalise_text(new_text[key]["title"])
        new_author = normaliser.normalise_authors(new_text[key]["authors"])
        new_subjs = list(new_text[key]["subjs"].values())
        for sub in new_subjs:
            sub = normaliser.normalise_text(sub)
            new_abstract.extend(sub)

        """record parameter"""

        title_len_diff = int(len(new_title) - len(old_title))
        abs_len_diff = int(len(new_abstract) - len(old_abstract))
        author_len_diff = int(len(new_author) - len(old_author))

        title_len_diff_sum = title_len_diff_sum + title_len_diff
        abs_len_diff_sum = abs_len_diff_sum + abs_len_diff
        author_len_diff_sum = author_len_diff_sum + author_len_diff


        """delete word in old text"""
        delete_word_index(title_dict, old_title, doc_id)
        delete_word_index(abs_dict, old_abstract, doc_id)
        delete_word_index(author_dict, old_author, doc_id)

        """init word in new text"""
        init_index(doc_id, new_title, title_dict)
        init_index(doc_id, new_abstract, abs_dict)
        init_index(doc_id, new_author, author_dict)


    """update total document length"""


    param_dict['abl'] = param_dict['abl'] + abs_len_diff_sum
    param_dict['til'] = param_dict['til'] + title_len_diff_sum
    param_dict['aul'] = param_dict['aul'] + author_len_diff_sum

    return

def write(filepath, word_dict): # file path with '*.pkl'
    with open(filepath,"wb") as f_wrindex:
         pickle.dump(word_dict,f_wrindex)
    f_wrindex.close()

def read_index_file(filepath):
    """read the index back to the dictinoary"""
    with open(filepath, "rb") as f:
        text = f.read()
        dict = pickle.loads(text)
        f.close()
        return dict


# start_time = time.time()
# initialise("/Users/AlisonLee/Desktop/ttdsdata/2016/1601.json")
# write("/Users/AlisonLee/Desktop/1601index.pkl",title_dict)
# print(read_index_file("/Users/AlisonLee/Desktop/1601index.pkl"))
# initialise("/Users/AlisonLee/Desktop/1501.json")
# print(title_dict)
# print(param_dict)
# update("/Users/AlisonLee/Desktop/1501.json", "/Users/AlisonLee/Desktop/1501new.json")
# print(title_dict)
# print(param_dict)

# print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == "__main__":
    start_time = time.time()
    from os import listdir
    from os.path import isfile, join
    mypath = "../../data/"
    # datafiles = [f for f in listdir(mypath) if isfile(join(mypath, f)) and '.json' in f]
    # for datafile in datafiles:
    #     initialise(mypath+datafile)
    # write(mypath+"title_dict", title_dict)
    # write(mypath+"author_dict", author_dict)
    # write(mypath+"abs_dict", abs_dict)
    # write(mypath+"param_dict", param_dict)
    # print("--- %s seconds ---" % (time.time() - start_time))
    # read_index_file(mypath+"title_dict")
    # read_index_file(mypath+"author_dict")
    # read_index_file(mypath+"abs_dict")
    # read_index_file(mypath+"param_dict")