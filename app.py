from flask import Flask, json
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Flask says Hello!!!</p>"

@app.route("/ditto")
def ditto():
    soup = BeautifulSoup("<p>Some<b>bad<i>HTML")
    print(soup.prettify())
    res = requests.get("https://pokeapi.co/api/v2/pokemon/ditto")
    return res.text

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)