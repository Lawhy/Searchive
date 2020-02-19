import pymongo
from normalise import Normaliser
import os

import json
import time

myclient = pymongo.MongoClient('mongodb://localhost:27017/')

db = myclient["ttds"]

def read(filepath):
    with open(filepath, "r") as f:
        json_text = f.read()
        text = json.loads(json_text)
        f.close()
    return text


# Deprecated
def init_index_delta(doc_id, text, ref):
    word_cnt = 0
    for pos, word in enumerate(text):
        word_cnt = word_cnt + 1
        if (ref.count_documents({ "_id": word}) == 0):
            ref.insert_one(
                {
                    '_id': word,
                    'df': 1,
                    doc_id: {
                        'tf': 1,
                        'pos': [pos],
                        'prevpos': pos
                    }
                }
            )
        elif ref.count_documents({ "_id": word, doc_id:{"$exists": False}}) == 0:
            prevpos = ref.find_one({ "_id": word})[doc_id]['prevpos']
            deltapos = pos - prevpos
            ref.update_one({"_id": word},
                               {'$inc':{
                                   'df': 1,
                                    doc_id + '.tf': 1
                               },
                                   '$push': {doc_id + '.pos': deltapos},
                                   '$set': {doc_id+'.prevpos': pos}
                               }

                           )
        elif ref.count_documents({ "_id": word, doc_id:{"$exists": True}}) == 0:
            """doc id not exists"""
            ref.update_one({"_id": word},
                           {'$inc': {
                               'df': 1,
                               doc_id + '.tf': 1
                           },
                               '$push': {doc_id + '.pos': pos},
                               '$set':{doc_id+'.prevpos': pos}
                           }

                           )
        else:
            print("not valid situation")

    return word_cnt


def delete_word_index(ref, old_text, doc_id):
    print(old_text)
    for word in old_text:
        tf_decre = ref.find_one({"_id": word})[doc_id]["tf"]
        ref.update_one({"_id": word},
            {'$unset':
                 {
                    doc_id : 1
                 },
                '$inc': {"df" : -tf_decre}
        })
    return

def init_index(doc_id, text, ref):

    word_cnt = 0
    for pos, word in enumerate(text):
        word_cnt = word_cnt + 1


        if ref.count_documents({ "_id": word}) > 0:
            """the word exists in the collection"""

            ref.update_one({"_id": word},
                                   {'$inc':{
                                       'df': 1,
                                        doc_id + '.tf': 1
                                   },
                                    '$push': {doc_id + '.pos': pos}
                                   }

                               )

        else:
            """the word appears for the first time"""

            ref.insert_one(
                {
                    '_id': word,
                    'df': 1,
                    doc_id: {
                        'tf': 1,
                        'pos': [pos],

                    }
                }
            )
    return word_cnt


def initialise(filename):
    """
  Initialise index
  index start from 0
  """
    start_time = time.time()
    normaliser = Normaliser()

    abs_colle_ref = db['abstract']
    title_colle_ref = db['title']
    author_colle_ref = db['author']

    param_ref = db['param']


    doc_total = 0
    total_title_word = 0
    total_abs_word = 0
    total_author_word = 0

    text = read(filename)


    for key in text.keys():
        if(doc_total>10):
            break

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
        # 还差update


        """creating index"""
        file_title_cnt = init_index(doc_id, title, title_colle_ref)
        file_abs_cnt = init_index(doc_id, abstract, abs_colle_ref)
        file_author_cnt = init_index(doc_id, author, author_colle_ref)
        total_abs_word = total_abs_word + file_abs_cnt
        total_title_word = total_title_word + file_title_cnt
        total_author_word = total_author_word + file_author_cnt




    param_ref.update_one(
                {'_id': 'abstract'},

                {'$inc': {
                    'total_doc_number': doc_total,
                    'total_document_length': total_abs_word
                }
            }
    )

    param_ref.update_one(
        {'_id': 'title'},

        {'$inc': {
            'total_doc_number': doc_total,
            'total_document_length': total_title_word
        }
        }
    )

    param_ref.update_one(
        {'_id': 'author'},

        {'$inc': {
            'total_doc_number': doc_total,
            'total_document_length': total_author_word
        }
        }
    )


    print("--- %s seconds ---" % (time.time() - start_time))
    return


def update(oldfile, newfile):

    normaliser = Normaliser()

    abs_colle_ref = db['abstract']
    title_colle_ref = db['title']
    author_colle_ref = db['author']

    param_ref = db['param']

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
        delete_word_index(title_colle_ref, old_title, doc_id)
        delete_word_index(abs_colle_ref, old_abstract, doc_id)
        delete_word_index(author_colle_ref, old_author, doc_id)

        """init word in new text"""
        init_index(doc_id, new_title, title_colle_ref)
        init_index(doc_id, new_abstract, abs_colle_ref)
        init_index(doc_id, new_author, author_colle_ref)


    """update total document length"""

    param_ref.update_one(
        {'_id': 'abstract'},

        {'$inc': {
            'total_document_length': abs_len_diff_sum
        }
        }
    )

    param_ref.update_one(
        {'_id': 'title'},

        {'$inc': {
            'total_document_length': title_len_diff_sum
        }
        }
    )

    param_ref.update_one(
        {'_id': 'author'},

        {'$inc': {
            'total_document_length': author_len_diff_sum
        }
        }
    )


    return



"""customise the filepath yourself"""
initialise("/Users/AlisonLee/Desktop/ttdsdata/2016/1601.json")

#update(old_file_path, new_file_path)
#delete_word_index(db["title"],["binari"],"1601-00007")
