# search-engine
TTDS coursework 3 

1. Data 
Link to data: https://drive.google.com/open?id=1T8EJ3_5EpNiGH5ggbPhZrLmPMzOMqtMe <br>
Link to glove embeddings: http://nlp.stanford.edu/data/glove.6B.zip
* Please use the 'preprocessed' version of data, each file an ordered dict in json format, a data sample is:
```r
# format:
   ID: {title (str), abstract (str), primary subject (dict), subjects (dict)}
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
2. Testing
* To test the application you need to create a folder called data in the same directory "search-engine" is in.
In data folder you need to get two create two files: test.json and glove.6B.50d.txt

3. Search Types
* General Search (title + author + abs + subjs)
* Title Search (title)
* Author Search (author)
* Abstract Search (abs + subjs)
   ##### Note that *subjects* can serve as a filter of search
   
4. Language Model for Similarity Search 
5. Spelling Correction
6. ...
