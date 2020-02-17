import re

from nltk.stem.snowball import EnglishStemmer
from nltk.corpus import stopwords
import nltk

stop_words = list(set(stopwords.words('english')))
class Normaliser:

    def __init__(self, stemmer=EnglishStemmer(), stop_words=stop_words, lower_case=True):
        self.stemmer = stemmer
        self.stop_words = stop_words
        self.lower_case = lower_case

    def clean_latex(self, text):
        latex_sents = re.findall(r'\$.+?\$', text)
        for sent in latex_sents:
            text = text.replace(sent, '')
        return text

    def normalise_token(self, token):
        if self.lower_case:
            token = token.lower()
        if token in self.stop_words:
            return None
        if self.stemmer:
            token = self.stemmer.stem(token)
        return token

    def normalise_text(self, text):
        if '$' in text:
            text = self.clean_latex(text)
        text = text.replace('\n', '')
        toks = re.findall(r'\w+', text)
        result = []
        for tok in toks:
            tok = self.normalise_token(tok)
            # incase None
            if tok:
                result.append(tok)
        return result

    def normalise_author(self, author):
        if self.lower_case:
            return author.lower()
