import re

from nltk.stem import *
from nltk.corpus import stopwords

def get_query(filepath_query):
    query = read(filepath_query)
    """ preprocessing """
    tokenised_text = re.findall("\w+",query)  # split on all the non-letter words, keep the words consisting of numbers or/and letters
    lowered_text = [w.lower() for w in tokenised_text]  # case folding
    stopped_text = [word for word in lowered_text if word not in stopwords]  # remove stop words
    stemmer = PorterStemmer()
    stemmed_text = [stemmer.stem(word) for word in stopped_text]  # stemming
    return stemmed_text