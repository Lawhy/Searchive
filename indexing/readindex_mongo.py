
import pymongo

myclient = pymongo.MongoClient('mongodb://localhost:27017/')

db = myclient["ttds"]

"""
mode = 'abstract' / 'title' / 'author'/ 'param'
"""

def read_index(word, mode):
    coll_ref = db[mode]

    doc_dict = coll_ref.find_one({"_id":word})
    print(doc_dict)
    return doc_dict

read_index("gama","title")