
import pymongo

myclient = pymongo.MongoClient('mongodb://localhost:27017/')

db = myclient["ttds_pos"]

"""
mode = 'abstract' / 'title' / 'author'/ 'param'
"""

def read_index(word, mode):
    coll_ref = db[mode]
    doc_dict = coll_ref.find_one({"_id":word})
    return doc_dict
