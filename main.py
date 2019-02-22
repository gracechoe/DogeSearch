#go through bookkeeping json in loop
#access file through given path in bookkeeping key
#use beautiful soup to parse through content of file
#extract tokens from file content
#add to list of corresponding postings for token key
#corresponding postings list include: document name/id token was found in, word frequency, 
#indices of occurence within the document, tf-idf score
#store this shit in a database (probably MongoDB)
import json
from bs4 import BeautifulSoup
import nltk
import re

def access_files():
    path = "/Users/macbookpro/Documents/WEBPAGES_RAW/"
    bookkeeping = open(path+"bookkeeping.json", "r")
    data = json.load(bookkeeping)
    #for key in data:
    parse_file(path+"0/33")

def parse_file(path):
    freq_dict = {}
    f = open(path)
    soup = BeautifulSoup(f.read(), "html.parser")
    soup.prettify()
    text = find_tags(soup).encode('utf-8')
    tokens = re.findall(r"[A-Za-z0-9]+", text.lower())
    for token in tokens:
        if token in freq_dict:
            freq_dict[token] += 1
        else:
            freq_dict[token] = 1
    print(freq_dict)

def find_tags(soup):
    [s.extract() for s in soup(['style', 'script', 'head'])]
    result = soup.get_text()
    return result

if __name__ == "__main__":
    access_files()