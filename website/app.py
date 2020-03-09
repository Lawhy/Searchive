import sys
sys.path.append('..')
from flask import Flask, render_template, url_for, request, redirect
import datetime as dt
import json
from collections import OrderedDict
import numpy as np
from scipy import spatial
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from operator import itemgetter
from spellchecker import SpellChecker
from ranking.ranking_local import search_for_detail

app = Flask(__name__)

embeddings_dict = {}

spell = SpellChecker()

class FixSizeOrderedDict(OrderedDict):
    def __init__(self, *args, max=0, **kwargs):
        self._max = max
        super().__init__(*args, **kwargs)

    def __setitem__(self, key, value):
        OrderedDict.__setitem__(self, key, value)
        if self._max > 0:
            if len(self) > self._max:
                self.popitem(False)

cached = FixSizeOrderedDict(max = 50)

with open("../../data/glove.6B.50d.txt", 'r') as f:
    for line in f:
        values = line.split()
        word = values[0]
        vector = np.asarray(values[1:], "float32")
        embeddings_dict[word] = vector

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/result', methods=['GET'])
def result():
    try:
        mode = request.args.get('mode')
        if mode == None:
            mode = 'abstract'
    except:
        mode = 'abstract'

    try:
        startIndex = int(request.args.get('si'))
    except:
        startIndex = 0

    try:
        numberOfResultsPerPage = int(request.args.get('rpp'))
    except:
        numberOfResultsPerPage = 10

    try:
        correctionFlag = request.args.get('correctionFlag')
    except:
        correctionFlag = None

    try:
        mode = request.args.get('mode')
        if mode == None:
            mode = 'general'
    except:
        mode = 'general'

    try:
        method = request.args.get('method')
        if method == None:
            method = 'mix'
    except:
        method = 'mix'

    try:
        sort = request.args.get('sort')
        if sort == None:
            sort = 'Relevance'
    except:
        sort = 'Relevance'

    try:
        query = request.args.get('q')
        if not query.strip():
            return redirect('/')
        else:
            misspelled = spell.unknown(query.strip().split())
            if len(misspelled) != 0 and correctionFlag == None and '"' not in query and mode != 'author':
                print(correctionFlag)
                correction = ' '.join([spell.correction(word) for word in query.strip().split()])
            else:
                correction = None
    except:
        return redirect('/')

    print(correction)
    print(query)

    print('mode',mode)
    print('method',method)

    if correction:
        if correction+mode+method in cached:
            results = cached[correction+mode+method]
        else:
            results = getResult(correction, mode, method)
            # for term in correction.split():
            #     for result in results:
            #         result['abs'] = result['abs'].replace(term, "<b>"+term+"</b>")
            cached[correction+mode+method] = results
    else:
        if query+mode+method in cached:
            results = cached[query+mode+method]
        else:
            results = getResult(query, mode, method)
            # for term in query.split():
            #     for result in results:
            #         result['abs'] = result['abs'].replace(term, "<b>"+term+"</b>")
            cached[query+mode+method] = results

    if sort == 'Relevance':
        pass
    elif sort == 'NtO':
        results = sorted(results, key=itemgetter('id'),  reverse=True) 
    else:
        results = sorted(results, key=itemgetter('id'))


    numberOfResults = len(results)

    # if len(query.split()) <= 5:
    #     closest_words = {}
    #     for idx, word in enumerate(query.split()):
    #         closest_words[idx] = find_closest_embeddings(embeddings_dict[word])[1:10]
    #     print(closest_words)

    resultsPerPage = results[startIndex:startIndex+numberOfResultsPerPage]

    # return render_template('test.html', results=resultsPerPage)

    return render_template('result.html', datetime=dt, title='result', results=resultsPerPage
    , startIndex=startIndex, numberOfResultsPerPage=numberOfResultsPerPage, numberOfResults=numberOfResults, query=query, 
    correction=correction, mode=mode, method=method, sort=sort, correctionFlag=correctionFlag)

@app.route('/about')
def about():
    return render_template('about.html')

def getResult(q,mode='general',method='tfidf'):
    data = search_for_detail(q,mode,method)
    return data

def find_closest_embeddings(embedding):
    return sorted(embeddings_dict.keys(), key=lambda word: spatial.distance.euclidean(embeddings_dict[word], embedding))

if __name__ == '__main__':
    try:
        app.run(debug=True)
    except:
        raise Exception("Restart the server soon.")
        exit(1)
