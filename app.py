import re
import json
from pymongo import MongoClient
from collections import defaultdict
from nltk.stem.snowball import SnowballStemmer
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

path = "/Users/gracechoe/Documents/WEBPAGES_RAW/"
bookkeeping = open(path+"bookkeeping.json", "r")
data = json.load(bookkeeping)
client = MongoClient("mongodb://localhost:27017/")
db = client["INVERTED_INDEX"]
index_col = db["index"]
doc_col = db["docs"]
stemmer = SnowballStemmer("english")

# retrieves all urls that contain the token, returns a string with 20 of those urls and total url count
@app.route("/get_urls/<tokens>")
def get_urls(tokens):
    global data
    result = []
    count = 0
    tokens = re.findall(r"[A-Za-z0-9]+", tokens.decode('utf-8').lower())

    query_dict = compute_queries(tokens)
    ranked = sorted(query_dict.items(), key=lambda k: (-k[1][1], -k[1][0]))

    for doc, _ in ranked:
        if count < 20:
            result.append(data[doc])
        count += 1
    return jsonify(result)


# creates a dictionary of documents with the respective td-idf and token count
def compute_queries(tokens):
    global index_col
    global stemmer
    d = defaultdict(list)
    for token in tokens:
        entry = index_col.find_one({'token': stemmer.stem(token)})
        if entry:
            for doc, tf_idf in zip(entry["documents"], entry["tf-idf"]):
                if doc in d:
                    d[doc][0] += tf_idf
                    d[doc][1] += 1
                else:
                    d[doc] = [tf_idf, 1]
    return d

if __name__ == "__main__":
    app.run(host='0.0.0.0')