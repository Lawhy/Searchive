from flask import Flask, render_template, url_for, request
import datetime as dt
import json

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/result', methods=['GET'])
def result():
    results = getResult(1)

    startIndex = 0

    numberOfResultsPerPage = 10

    query = 'deep learning'

    if request.args.get('si'):
        try:
            startIndex = int(request.args.get('si'))
        except:
            startIndex = 0

    if request.args.get('rpp'):
        try:
            numberOfResultsPerPage = int(request.args.get('rpp'))
        except:
            numberOfResultsPerPage = 10

    if request.args.get('q'):
        try:
            query = request.args.get('q')
        except:
            query = 'deep learning'

    numberOfResults = len(results)

    return render_template('result.html', datetime=dt, title='result', results=results[startIndex:startIndex+numberOfResultsPerPage]
    , startIndex=startIndex, numberOfResultsPerPage=numberOfResultsPerPage, numberOfResults=numberOfResults, query=query)

@app.route('/about')
def about():
    return render_template('about.html')

def getResult(q):
    with open('../../data/test.json') as f:
        data = json.load(f)
    return data

if __name__ == '__main__':
    app.run(debug=True)
