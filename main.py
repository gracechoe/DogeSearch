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

def access_files():
    path = "/Users/macbookpro/Documents/WEBPAGES_RAW/"
    bookkeeping = open(path+"bookkeeping.json", "r")
    data = json.load(bookkeeping)
    for key in data:
        parse_file(path+key)

def parse_file(path):
    f = open(path)
    soup = BeautifulSoup(f.read(), "html.parser")
    soup.prettify()
    #print(soup.get_text())
    print(find_tags(soup))


def find_tags(soup):
    result = soup.findAll(["body", "title", "h1", "h2", "h3", "b", "strong"])
    #return result
    return soup

if __name__ == "__main__":
    access_files()