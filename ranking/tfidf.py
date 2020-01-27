import json
import math
import time

def read(file):
    with open(filepath,"r") as f:
        text = f.read()
        f.close()
    return text

def score_cal(df,tf):
    if df != 0 and tf != 0:
        w = (1 + math.log(float(tf),10))*math.log(5000/float(df),10)
        return w
    else:
        return 0
    
def rank(json_text):
    rank_dict = {}
    text = json.loads(json_text)
    for key in text.keys():
        word = key
        df = text[key]["df"]
        print("word: %s" % word)
        score = 0
        for keys in text[key]["docdict"].keys():
            tf = text[key]["docdict"][keys]["tf"]
            score += score_cal(df,tf)
        print("doc_id: %s score: %f" % keys, score)
        rank_dict[key] = score

def write(filepath,rank_dict):
    with open(filepath,"w") as f_wrindex:
         json.dump(rank_dict,f_wrindex)
    f_wrindex.close()
    
start_time = time.time()
text = read(filepath)
rank_dict = rank(text)
write(filepath,rank_dict)
print("--- %s seconds ---" % (time.time() - start_time))


        