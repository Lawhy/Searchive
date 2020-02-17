import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


cred = credentials.Certificate("/Users/AlisonLee/Downloads/searchive-e90e4-firebase-adminsdk-pz1m9-6a24ab72e1.json")
project_id = "searchive-e90e4"

firebase_admin.initialize_app(cred, {
    'projectId': project_id,
})

db = firestore.client()


"""
mode = 'abstract' / 'title' / 'author'/ 'param'

"""

def read_index(word, mode):
    doc_ref = db.collection(mode).document(word)
    try:
        doc = doc_ref.get()
        doc_dict = doc.to_dict()

    except google.cloud.exceptions.NotFound:
        print('No such word in index file!')
    return doc_dict





    return param_dict


