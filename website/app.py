from flask import Flask, render_template, url_for, request, redirect
import datetime as dt
import json
import torch
import numpy as np
from scipy import spatial
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE

app = Flask(__name__)

embeddings_dict = {}
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
    results = getResult(1)

    try:
        startIndex = int(request.args.get('si'))
    except:
        startIndex = 0

    try:
        numberOfResultsPerPage = int(request.args.get('rpp'))
    except:
        numberOfResultsPerPage = 10

    try:
        query = request.args.get('q')
        if not query.strip():
            return redirect('/')
    except:
        return redirect('/')

    numberOfResults = len(results)

    # if len(query.split()) <= 5:
    #     closest_words = {}
    #     for idx, word in enumerate(query.split()):
    #         closest_words[idx] = find_closest_embeddings(embeddings_dict[word])[1]
    #     print(closest_words)

    return render_template('result.html', datetime=dt, title='result', results=results[startIndex:startIndex+numberOfResultsPerPage]
    , startIndex=startIndex, numberOfResultsPerPage=numberOfResultsPerPage, numberOfResults=numberOfResults, query=query)

@app.route('/about')
def about():
    return render_template('about.html')

def getResult(q):
    with open('../../data/test.json') as f:
        data = json.load(f)
    return data

def find_closest_embeddings(embedding):
    return sorted(embeddings_dict.keys(), key=lambda word: spatial.distance.euclidean(embeddings_dict[word], embedding))

if __name__ == '__main__':
    app.run(debug=True)
