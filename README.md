# Searchive
TTDS coursework 3:

1. Data 
Link to data: ... <br>
Link to glove embeddings: http://nlp.stanford.edu/data/glove.6B.zip <br>
URL format to papers: https://arxiv.org/abs/{ID} <br>
e.g. https://arxiv.org/abs/1901.00001 <br>
* Please use the 'preprocessed' version of data, each file an ordered dict in json format, a data sample is:
```r
# format:
   ID: {title (str), authors (list(str)), abstract (str), primary subject (dict), subjects (dict)}
# example:
{
"1901.00001": {"title": "some text ...", 
               "authors": ["author1", ...]
               "abs": "some text ...", 
               "1st_subj": {"cs.CV": "Computer Vision and Pattern Recognition"}, 
               "subjs": {"cs.CV": "Computer Vision and Pattern Recognition", "cs.LG": "Machine Learning", "stat.ML": "Machine Learning"}}},
...
}
```
2. Import Our Own Modules
```r
# example to use the Normaliser class in normalise.py in the folder preprocess 
import sys
sys.path.append('..')  # append the main directory path
from preprocess.normalise import Normaliser
```
To use the Normaliser, simply:
```r
norm = Normaliser()
...
# get tokens from the raw text
clean_text = norm.normalise_text(text)
```

3. Testing
* To test the application you need to create a folder called data in the same directory "search-engine" is in.
In data folder you need to get two create two files: test.json and glove.6B.50d.txt

4. Search Types
* General Search (title + author + abs + subjs)
* Title Search (title)
* Author Search (author)
* Abstract Search (abs + subjs)
* ~~Fuzzy Search~~
   ##### Note that *subjects* can serve as a filter of search
5. Language Model for Similarity Search 
6. Spelling Correction
7. ...

--------------------
### Email from Walid:
You are not allowed to use search engine libraries that does index or search. 
However, you are allowed to use libraries for secondary features, such as autocomplete or spelling correction.

### To successfully run firestore
* Do not use DICE! (you don't have root access)
* pip install firebase_admin
* Download the json public key file shared in the groupchat

### To install and run mongdb:
configure your local mongdb: https://www.runoob.com/mongodb/mongodb-osx-install.html
use python to operate on your local mongodb: https://api.mongodb.com/python/current/tutorial.html

### merge.json
Link of data: https://drive.google.com/open?id=1szTszClFYDPWeUX9P_NizAKVXhG7UffM

### Final Feedback:
Group ID: 2 <br><br>

Number of students: 5 <br><br>

Positive: <br><br>

- Nice and clear report <br><br>

- The idea is very interesting <br><br>

- Having evaluation section <br><br>

Negative: <br><br>

Comments: <br><br>

Excellent work. <br><br>

There are other features that could be added such as author suggestion in the query. <br><br>

It might be useful to cinsider graphical explanation for the implemented system (i.e. to show the different modules and how they interact with each other. <br><br>

Well done! <br><br>

Overall group mark (15): 13 <br>
