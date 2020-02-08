import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from normalise import Normaliser

import json
import os

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


def initialise(directory):
    """
  Initialise index
  """
    normaliser = Normaliser()
    abs_colle_ref = db.collection('abstract')
    title_colle_ref = db.collection('title')
    abs_param_ref = db.collection('param').document("abstract")
    title_param_ref = db.collection('param').document("title")

    # TODO: author

    doc_total = 0
    total_title_word = 0
    total_abs_word = 0

    for filename in os.listdir(directory):
        text = read(filename)
        for key in text.keys():
            doc_total = doc_total + 1
            doc_id = key.replace(".", "-")
            abstract = normaliser.normalise_text(text[key]["abs"])
            title = normaliser.normalise_text(text[key]["title"])

            # TODO : author

            """creating index"""

            file_title_cnt = init_index(doc_id, title, title_colle_ref)
            file_abs_cnt = init_index(doc_id, abstract, abs_colle_ref)
            total_abs_word = total_abs_word + file_abs_cnt
            total_title_word = total_title_word + file_title_cnt

            if doc_total > 3:
                break

    abs_param_ref.set(
        {
            'total doc number': doc_total,
            'total document length': total_abs_word
        }
    )

    title_param_ref.set(
        {
            'total doc number': doc_total,
            'total document length': total_title_word
        }
    )

    return


def update(oldfile, newfile):
    normaliser = Normaliser()
    old_text = read(oldfile)
    new_text = read(newfile)
    for key in old_text.keys():
        doc_id = key.replace(".", "-")
        old_abstract = normaliser.normalise_text(old_text[key]["abs"])
        old_title = normaliser.normalise_text(old_text[key]["title"])
        new_abstract = normaliser.normalise_text(new_text[key]["abs"])
        new_title = normaliser.normalise_text(new_text[key]["title"])

        title_to_update = set(old_title).union(new_title)
        abs_to_update = set(old_abstract).union(new_abstract)

        title_to_delete = set(title_to_update).difference(new_title)
        abs_to_delete = set(abs_to_update).difference(new_abstract)

        # scan again and add other elements

        # title_to_add = set(title_to_update).difference(old_title)
        # abs_to_add = set(abs_to_update).difference(old_abstract)

    return


initialise("/Users/AlisonLee/Desktop/ttds_initial_data")
