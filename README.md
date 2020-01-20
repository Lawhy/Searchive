# search-engine
TTDS coursework 3

1. Link to data: https://drive.google.com/open?id=1T8EJ3_5EpNiGH5ggbPhZrLmPMzOMqtMe
* Please use the 'preprocessed' version of data, each file an ordered dict in json format, a data sample is:
```r
# format:
   ID: {title (str), abstract (str), primary subject (dict), subjects (dict)}
# example:
{
"1901.00001": {"title": "some text ...", 
               "abs": "some text ...", 
               "1st_subj": {"cs.CV": "Computer Vision and Pattern Recognition"}, 
               "subjs": {"cs.CV": "Computer Vision and Pattern Recognition", "cs.LG": "Machine Learning", "stat.ML": "Machine Learning"}}},
...
}
```

