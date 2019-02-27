import json
path = "/Users/gracechoe/Documents/WEBPAGES_RAW/"
bookkeeping = open(path+"bookkeeping.json", "r")
data = json.load(bookkeeping)
count = 0
for key in data:
    if count == 1575:
        print("1575: ", key)
    if count == 1576:
        print("1576: ", key)
    if count == 1577:
        print("1577: ", key)
        break
    count += 1
    print(count)
