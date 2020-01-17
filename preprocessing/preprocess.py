import re
import json
import pickle
from dicttoxml import dicttoxml

class ArxivPreprocessor:

    def __init__(self, _dir, yymm):
        with open(_dir + '/' + yymm + '.json', 'r', encoding='UTF-8') as f:
            self.dict = json.load(f)
        self.size = len(self.dict)

    def get_id(self, i):
        return self.dict[i]['id']

    def get_title(self, i):
        return self.dict[i]['title'][0].replace('\n', '').strip()

    def get_abs(self, i):
        return self.dict[i]['abstract'][0]

    def get_1st_subj(self, i):
        fst_subj = self.read_subj(self.dict[i]['primary_subject'][0])
        return {fst_subj[1]: fst_subj[0]}

    def get_subjs(self, i):
        subjs = self.dict[i]['subjects']
        return {self.read_subj(s)[1]: self.read_subj(s)[0] for s in subjs}

    # turn all the documents into usable format
    def preprocess(self):
        result = dict()
        for i in range(self.size):
            result[self.get_id(i)] = {
                'title': self.get_title(i),
                'abs': self.get_abs(i),
                '1st_subj': self.get_1st_subj(i),
                'subjs': self.get_subjs(i)
            }
        return result

    @classmethod
    def read_subj(cls, subj):
        return re.findall('(.+) \((.+)\)', subj)[0]


a = ArxivPreprocessor('../../data', "1901")
# print(a.get_title(11))
# print(a.get_1st_subj(11))
# print(a.get_subjs(11))
result = a.preprocess()
print(type(result))
print(result['1901.00003'])
with open('1901.json', 'w+') as f:
    json.dump(result, f)
