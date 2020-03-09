import pymongo
import sys
sys.path.append('..')
from preprocess.normalise import Normaliser

import json
import time

myclient = pymongo.MongoClient('mongodb://localhost:27017/')

"""you clinet name"""
db = myclient["ttds_pos"]


"""read file"""
def read(filepath):
    with open(filepath, "r") as f:
        json_text = f.read()
        text = json.loads(json_text)
        f.close()
    return text


def delete_word_index(ref, old_text, doc_id):

    for word in set(old_text):
        ref.update_one({"_id": word},
            {'$unset':
                 {
                    doc_id : 1
                 }
        })
    return

def init_index(doc_id, text, ref):


    for pos, word in enumerate(text):

        if ref.count_documents({ "_id": word}) > 0:
            """the word exists in the collection"""

            ref.update_one({"_id": word},
                                   {
                                    '$push': {doc_id : pos}
                                   }
                               )

        else:
            """the word appears for the first time"""

            ref.insert_one(
                {
                    '_id': word,
                    doc_id: [pos]
                }
            )
    return


"""initialise index, input file path"""
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
        init_index(doc_id, title, title_colle_ref)
        init_index(doc_id, abstract, abs_colle_ref)
        init_index(doc_id, author, author_colle_ref)


    print("--- %s seconds ---" % (time.time() - start_time))
    return

"""update index, input old file path and new file path"""
def update(oldfile, newfile):

    normaliser = Normaliser()

    abs_colle_ref = db['abstract']
    title_colle_ref = db['title']
    author_colle_ref = db['author']

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
        delete_word_index(title_colle_ref, old_title, doc_id)
        delete_word_index(abs_colle_ref, old_abstract, doc_id)
        delete_word_index(author_colle_ref, old_author, doc_id)

        """init word in new text"""
        init_index(doc_id, new_title, title_colle_ref)
        init_index(doc_id, new_abstract, abs_colle_ref)
        init_index(doc_id, new_author, author_colle_ref)



    return





# """customise the data filepath yourself"""
# """you can write a function to loop over all the files in your data repo"""
# initialise("/Users/AlisonLee/Desktop/1501.json")
# update("/Users/AlisonLee/Desktop/1501.json", "/Users/AlisonLee/Desktop/1501new.json")

if __name__ == "__main__":
    start_time = time.time()
    from os import listdir
    from os.path import isfile, join
    mypath = "../../data/"
    datafiles = [f for f in listdir(mypath) if isfile(join(mypath, f)) and '.json' in f]
    for datafile in datafiles:
        initialise(mypath+datafile)