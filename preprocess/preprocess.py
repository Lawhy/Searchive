import re
import json
from collections import OrderedDict

class ArxivPreprocessor:

    def __init__(self, _dir, yymm):
        with open(_dir + '/' + yymm + '.json', 'r', encoding='UTF-8') as f:
            self.dict = json.load(f)
        self.size = len(self.dict)

    def get_id(self, i):
        return self.dict[i]['id']

    def get_authors(self, i):
        return self.dict[i]['authors']

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
                'authors': self.get_authors(i),
                'abs': self.get_abs(i),
                '1st_subj': self.get_1st_subj(i),
                'subjs': self.get_subjs(i)
            }
        return OrderedDict(sorted(result.items(), key=lambda x: x[0]))

    @classmethod
    def read_subj(cls, subj):
        return re.findall('(.+) \((.+)\)', subj)[0]


if __name__ == '__main__':
    for year in ['14', '15', '16', '17', '18', '19']:
        for i in ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']:
            name = year + i
            a = ArxivPreprocessor('D:\\UOE\\arXiv_data\\raw\\20' + year, name)
            # print(a.get_title(11))
            # print(a.get_1st_subj(11))
            # print(a.get_subjs(11))
            result = a.preprocess()
            print(len(result), 'documents...')
            with open('D:\\UOE\\arXiv_data\\preprocessed\\20' + year + '\\' + name + '.json', 'w+') as f:
                json.dump(result, f)
