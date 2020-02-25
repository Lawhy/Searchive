import json
import time
import pickle
from normalise import Normaliser

abs_pos_dict = {}
title_pos_dict = {}
author_pos_dict = {}

def read(filepath):
    with open(filepath, "r") as f:
        json_text = f.read()
        text = json.loads(json_text)
        f.close()
    return text

"""structure {word:{doc_id : [pos]}}"""

def init_index_pos(doc_id, text, dict):

    for pos, word in enumerate(text):
        if word not in dict:
            """first time"""
            dict[word]={}
            dict[word][doc_id] = [pos]
        else:
            if doc_id not in dict[word]:
                """first document"""
                dict[word][doc_id]= [pos]
            else:
                dict[word][doc_id].append(pos)
    return


def delete_word_pos(dict, old_text, doc_id):
    for pos, word in enumerate(old_text):
        if word in dict.keys():
            if doc_id in dict[word].keys():
                dict[word].pop(doc_id,None)
                if dict[word] == {}:
                    dict.pop(word,None)
    return


def initialise_pos(filename):
    """
  Initialise index
  index start from 0
  """

    normaliser = Normaliser()
    text = read(filename)

    for key in text.keys():


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
        init_index_pos(doc_id, title, title_pos_dict)
        init_index_pos(doc_id, abstract, abs_pos_dict)
        init_index_pos(doc_id, author, author_pos_dict)


    print("--- %s seconds ---" % (time.time() - start_time))
    return



def update_pos(oldfile, newfile):

    normaliser = Normaliser()

    old_text = read(oldfile)
    new_text = read(newfile)


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


        """delete word in old text"""
        delete_word_pos(title_pos_dict, old_title, doc_id)
        delete_word_pos(abs_pos_dict, old_abstract, doc_id)
        delete_word_pos(author_pos_dict, old_author, doc_id)

        """init word in new text"""
        init_index_pos(doc_id, new_title, title_pos_dict)
        init_index_pos(doc_id, new_abstract, abs_pos_dict)
        init_index_pos(doc_id, new_author, author_pos_dict)

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


start_time = time.time()

initialise_pos("/Users/AlisonLee/Desktop/1501.json")
print(abs_pos_dict)

update_pos("/Users/AlisonLee/Desktop/1501.json", "/Users/AlisonLee/Desktop/1501new.json")
print(abs_pos_dict)


print("--- %s seconds ---" % (time.time() - start_time))