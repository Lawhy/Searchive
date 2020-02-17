import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from normalise import Normaliser
import os


import json

"""
Initialise firebase service
"""

# Use the application default credentials
cred = credentials.Certificate("/Users/AlisonLee/Downloads/searchive-e90e4-firebase-adminsdk-pz1m9-6a24ab72e1.json")
project_id = "searchive-e90e4"

firebase_admin.initialize_app(cred, {
    'projectId': project_id,
})

db = firestore.client()


def read(filepath):
    with open(filepath, "r") as f:
        json_text = f.read()
        text = json.loads(json_text)
        f.close()
    return text


def init_index(doc_id, text, ref):
    word_cnt = 0
    for pos, word in enumerate(text):
        word_cnt = word_cnt + 1
        word_doc_ref = ref.document(word)
        if word_doc_ref.get().exists:
            """the word exists in the collection"""
            word_doc_ref.update(
                {
                    'df': firestore.Increment(1),
                    doc_id: {
                        'tf': firestore.Increment(1),
                        'pos': firestore.ArrayUnion([pos])
                    }
                }
            )


        else:
            """the word appears for the first time"""
            word_doc_ref.set(
                {
                    'df': 1,
                    doc_id: {
                        'tf': 1,
                        'pos': [pos]
                    }
                }
            )

    return word_cnt


def initialise(filename):
    """
  Initialise index
  index start from 0
  """
    normaliser = Normaliser()

    abs_colle_ref = db.collection('abstract')
    title_colle_ref = db.collection('title')
    author_colle_ref = db.collection('author')

    abs_param_ref = db.collection('param').document("abstract")
    title_param_ref = db.collection('param').document("title")
    author_param_ref = db.collection('param').document("author")

    doc_total = 0
    total_title_word = 0
    total_abs_word = 0
    total_author_word = 0


    text = read(filename)

    for key in text.keys():
        doc_total = doc_total + 1
        doc_id = key.replace(".", "-")
        abstract = normaliser.normalise_text(text[key]["abs"])
        title = normaliser.normalise_text(text[key]["title"])
        author = normaliser.normalise_authors(text[key]["authors"])




        """creating index"""

        file_title_cnt = init_index(doc_id, title, title_colle_ref)
        file_abs_cnt = init_index(doc_id, abstract, abs_colle_ref)
        file_author_cnt = init_index(doc_id, author, author_colle_ref)
        total_abs_word = total_abs_word + file_abs_cnt
        total_title_word = total_title_word + file_title_cnt
        total_author_word = total_author_word + file_author_cnt


    abs_param_ref.set(
        {
            'total_doc_number': doc_total,
            'total_document_length': total_abs_word
        }
    )

    title_param_ref.set(
        {
            'total_doc_number': doc_total,
            'total_document_length': total_title_word
        }
    )

    author_param_ref.set(
        {
            'total_doc_number': doc_total,
            'total_document_length': total_author_word
        }
    )
    return


def delete_word_index(ref, old_text, doc_id):
    for word in old_text:
        word_doc_ref = ref.document(word)
        word_doc_ref.update({
            doc_id: firestore.DELETE_FIELD,
            "df": firestore.Increment(-1)
        })
    return


def update(oldfile, newfile):

    # TODO author
    normaliser = Normaliser()

    abs_colle_ref = db.collection('abstract')
    title_colle_ref = db.collection('title')
    author_colle_ref = db.collection('author')
    abs_param_ref = db.collection('param').document("abstract")
    title_param_ref = db.collection('param').document("title")
    author_param_ref = db.collection('param').document("author")

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

        new_abstract = normaliser.normalise_text(new_text[key]["abs"])
        new_title = normaliser.normalise_text(new_text[key]["title"])
        new_author = normaliser.normalise_authors(new_text[key]["authors"])

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
        init_index(doc_id,new_author, author_colle_ref)


    """update total document length"""

    title_param_ref.update({
        'total_document_length' : firestore.Increment(title_len_diff_sum)
    })

    abs_param_ref.update({
        'total_document_length': firestore.Increment(abs_len_diff_sum)
    })

    author_param_ref.update({
        'total_document_length': firestore.Increment(author_len_diff_sum)
    })

    # origin_title_total_length = title_param_ref.get(field_paths={'total document length'}).to_dict()
    # origin_abs_total_length = abs_param_ref.get(field_paths={'total document length'}).to_dict()
    #
    # new_title_total_length = int(origin_title_total_length["total document length"]) + title_len_diff_sum
    # new_abs_total_length = int(origin_abs_total_length["total document length"]) + abs_len_diff_sum
    #
    # title_param_ref.update({
    #         'total document length': new_title_total_length
    #     })
    #
    #
    # abs_param_ref.update({
    #     'total document length': new_abs_total_length
    # })


    return


# path = "/Users/AlisonLee/Desktop/ttdsdata"
# for dir in os.listdir(path):
#     if(dir != ".DS_Store"):
#         for file in os.listdir(path+"/"+dir):
#             print(file)
#             initialise(file)

#update("/Users/AlisonLee/Desktop/190101.json","/Users/AlisonLee/Desktop/190101new.json")

initialise("/Users/AlisonLee/Desktop/ttdsdata/2015/1501.json")