from flask import Flask
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route("/even_odd/<n>")
def is_even(n):
    n = int(n)
    if n % 2 == 0:
        return str(n) + " is even"
    else:
        return str(n) + " is odd"

app.run(host='0.0.0.0')