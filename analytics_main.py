from pymongo import MongoClient
import json

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
    print(output_str)
    log_file = open("analytics.txt", "w+")
    log_file.write(output_str)
    log_file.close()

def get_urls(token):
    client = MongoClient("mongodb://localhost:27017/")
    db = client["INVERTED_INDEX"]
    result = ""
    bookkeeping = open("/Users/gracechoe/Documents/WEBPAGES_RAW/bookkeeping.json", "r")
    data = json.load(bookkeeping)
    entry = db["index"].find_one({'token':token.lower()})
    if entry:
        documents = entry["documents"]
        count = 0
        for doc in documents:
            if count < 20:
                result += data[doc] + "\n"
                count += 1
        result += str(len(entry["documents"]))
    return result

if __name__ == "__main__":
    create_output_file()