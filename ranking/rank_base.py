import collections
import json
import re
import time
import numpy as np

from nltk.stem import *
from nltk.corpus import stopwords


def read(filepath):
    with open(filepath, "r") as f:
        text = f.read()
        f.close()

    return text

def parse(json_text):
    word_dict={}
    text = json.loads(json_text)
    for key in text.keys():
        doc_id = key    #string
        abstract = text[key]["abs"]
        """ preprocessing """
        tokenised_text = re.findall("\w+",abstract)  # split on all the non-letter words, keep the words consisting of numbers or/and letters
        lowered_text = [w.lower() for w in tokenised_text]  # case folding
        stopped_text = [word for word in lowered_text if word not in stopwords]  # remove stop words
        stemmer = PorterStemmer()
        stemmed_text = [stemmer.stem(word) for word in stopped_text]  # stemming


        # {word : {"df": xx, "docdict":{doc_id 1:{"tf": yy, "pos": [postlist]} , doc_id 2}}}


        """ create the positional inverted index """
        for pos, word in enumerate(stemmed_text):
            if word not in word_dict:
                word_dict[word] = {}
                word_dict[word]["df"] = 1
                word_dict[word]["docdict"]= {doc_id:{"pos" : [pos+1]}}
                word_dict[word]["docdict"][doc_id]["tf"] = 1
                #word_dict[word] = {"docdict":{doc_id: {"pos":[pos + 1]}}}
                #word_dict[word]["docdict"][doc_id].update({"tf":1})
                #word_dict[word]["df"]=1
            else:
                word_dict[word]["df"] = word_dict[word]["df"] + 1
                if doc_id not in word_dict[word]["docdict"]:
                    word_dict[word]["docdict"][doc_id]={"pos":[pos + 1]}
                    word_dict[word]["docdict"][doc_id]["tf"] = 1


                    #word_dict[word]["docdict"].update({doc_id: {"pos":[pos + 1]}})
                    #word_dict[word]["docdict"][doc_id].update({"tf":1})
                else:
                    word_dict[word]["docdict"][doc_id]["pos"].append(pos + 1)
                    word_dict[word]["docdict"][doc_id]["tf"] = word_dict[word]["docdict"][doc_id]["tf"]  + 1
    return word_dict

def write(filepath,word_dict):
    #np.save(filepath,word_dict)
    with open(filepath,"w") as f_wrindex:
         json.dump(word_dict,f_wrindex)
    f_wrindex.close()
    #     # for word, data in word_dict.items():
    #     #     f_wrindex.write(word + ":")
    #     #     f_wrindex.write(str(data["df"]))
    #     #     f_wrindex.write("\n")
    #     #
    #     #     for doc_id, doc_inf in data["docdict"].items():
    #     #         f_wrindex.write("\t")
    #     #         f_wrindex.write(doc_id + ": ")
    #     #         f_wrindex.write(str(doc_inf["tf"]))
    #     #         f_wrindex.write(" ")
    #     #         pos_list = doc_inf["pos"]
    #     #         f_wrindex.write(",".join([str(pos) for pos in pos_list]))
    #     #         f_wrindex.write("\n")
    #     #     f_wrindex.write("\n")


start_time = time.time()
text = read("/afs/inf.ed.ac.uk/user/s18/s1891132/Downloads/1901.json")
stopwords= set(stopwords.words('english'))
index_dict= parse(text)
#sorted_word_dict = collections.OrderedDict(sorted(index_dict.items()))
write("/afs/inf.ed.ac.uk/user/s18/s1891132/Downloads/index.json",index_dict)
print("--- %s seconds ---" % (time.time() - start_time))