import collections
import json
import re
import time

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
    #print(type(text))
    #print(text.keys())
    for key in text.keys():
        doc_id = key
        #title =  text[key]["title"]
        abstract = text[key]["abs"]
        """ preprocessing """
        tokenised_text = re.findall("\w+",abstract)  # split on all the non-letter words, keep the words consisting of numbers or/and letters
        lowered_text = [w.lower() for w in tokenised_text]  # case folding
        stopped_text = [word for word in lowered_text if word not in stopwords]  # remove stop words
        stemmer = PorterStemmer()
        stemmed_text = [stemmer.stem(word) for word in stopped_text]  # stemming

        """ create the positional inverted index """
        for pos, word in enumerate(stemmed_text):
            if word not in word_dict:
                word_dict[word] = {doc_id: [pos + 1]}
            else:
                if doc_id not in word_dict[word]:
                    word_dict[word].update({doc_id: [pos + 1]})
                else:
                    word_dict[word][doc_id].append(pos + 1)
    return word_dict

def write(filepath,word_dict):
    with open(filepath,"w") as f_wrindex:  # the third input argument in the command line is the text file path you want to write the index in
        for word, doc in word_dict.items():
            f_wrindex.write(word + ":")
            f_wrindex.write("\n")
            for doc_id, pos_list in doc.items():
                f_wrindex.write("\t")
                f_wrindex.write(doc_id + ": ")
                f_wrindex.write(",".join([str(pos) for pos in pos_list]))
                f_wrindex.write("\n")
            f_wrindex.write("\n")
    f_wrindex.close()

start_time = time.time()
text = read("/afs/inf.ed.ac.uk/user/s18/s1891132/Downloads/1901.json")
stopwords= set(stopwords.words('english'))
index_dict= parse(text)
sorted_word_dict = collections.OrderedDict(sorted(index_dict.items()))
write("/afs/inf.ed.ac.uk/user/s18/s1891132/Downloads/index.txt",sorted_word_dict)
print("--- %s seconds ---" % (time.time() - start_time))