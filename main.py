#go through bookkeeping json in loop
#access file through given path in bookkeeping key
#use beautiful soup to parse through content of file
#extract tokens from file content
#add to list of corresponding postings for token key
#corresponding postings list include: document name/id token was found in, word frequency, 
#indices of occurence within the document, tf-idf score
#store this shit in a database (probably MongoDB)
import os
import json

def access_files():
    path = "/Users/macbookpro/Documents/WEBPAGES_RAW/"
    bookkeeping = open(path+"bookkeeping.json", "r")
    data = json.load(bookkeeping)
    for key in data:
        f = open(path+key)
        print(f.read())
        

if __name__ == "__main__":
    access_files()