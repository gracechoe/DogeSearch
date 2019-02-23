import json
import re
import math
from bs4 import BeautifulSoup
from pymongo import MongoClient

def access_files():
    path = "/Users/gracechoe/Documents/WEBPAGES_RAW/"
    bookkeeping = open(path+"bookkeeping.json", "r")
    data = json.load(bookkeeping)
    count = 0
    for key in data:
        if count > 150:
            break
        process_file(path,key)
        count += 1
        print(count)
    complete_index()
    create_output_file()

def complete_index():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["INVERTED_INDEX"]
    col = db["index"]
    col2 = db["docs"]
    doc_count = col2.count()

    for entry in col.find():
        docs = entry['documents']
        freqs = entry['word_freq']
        token = entry['token']
        for doc, freq in zip(docs, freqs):
            result = col2.find({'doc': doc})
            result = result.next()
            term_count = result['terms_count']
            tf = float(freq) / term_count
            idf = math.log(float(doc_count)/len(docs))
            tf_idf = tf*idf
            col.update({'token':token},{"$push":{'tf-idf':tf_idf}})


def process_file(path, key):
    freq_dict = {}
    f = open(path+key)
    soup = BeautifulSoup(f.read(), "html.parser")
    try:
        soup.prettify()
        text = find_tags(soup)
        tokens = re.findall(r"[A-Za-z0-9]+", text.lower())
        for token in tokens:
            if token in freq_dict:
                freq_dict[token] += 1
            else:
                freq_dict[token] = 1

        client = MongoClient("mongodb://localhost:27017/")
        db = client["INVERTED_INDEX"]
        index_col = db["index"]
        doc_col = db["docs"]

        for token, freq in freq_dict.items():
            if index_col.find_one({'token': token}):
                query = {'token': token}
                new_values = {"$push": {'documents': key, 'word_freq': freq}}
                index_col.update_one(query, new_values)
            else:
                entry = {
                    'token': token, 'documents': [key], 'word_freq': [freq], 'tf-idf': []
                }
                result = index_col.insert(entry)

        entry = {'doc':key, 'terms_count':len(tokens)}
        doc_col.insert(entry)
    except:
        print("caught an error")
        pass


def find_tags(soup):
    [s.extract() for s in soup(['style', 'script', 'head'])]
    result = soup.get_text()
    return result

def create_output_file():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["INVERTED_INDEX"]
    output_str = "PROGRAM ANALYTICS"
    output_str += "\n Number of Documents: "
    output_str += str(db["docs"].find().count())
    output_str += "\n Number of Unique Words: "
    output_str += str(db["index"].find().count())
    output_str += "\n Total size of Index on Disk (in KB):"
    output_str += str(db.command({"collStats":"index", "scale":1024})["totalIndexSize"])
    output_str += "\n URL results for Query [Informatics]: \n"
    output_str += get_urls("Informatics")
    output_str += "\n URL results for Query [Mondego]: \n"
    output_str += get_urls("Mondego")
    output_str += "\n URL results for Query [Irvine]: \n"
    output_str += get_urls("Irvine")
    log_file = open("analytics.txt", "w+")
    log_file.write(output_str)
    log_file.close()

def get_urls(token):
    client = MongoClient("mongodb://localhost:27017/")
    db = client["INVERTED_INDEX"]
    result = ""
    bookkeeping = open("/Users/macbookpro/Documents/WEBPAGES_RAW/bookkeeping.json", "r")
    data = json.load(bookkeeping)
    entry = db["index"].find_one({'token':token.lower()})
    if entry:
        documents = entry["documents"]
        count = 0
        for doc in documents:
            if count < 20:
                result += data[doc] + "\n"
                count += 1
        result += entry["documents"].count()
    return result

if __name__ == "__main__":
    access_files()