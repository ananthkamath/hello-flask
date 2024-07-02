from flask import Flask, json
from bs4 import BeautifulSoup
import requests
from langchain_openai import ChatOpenAI
from sklearn.datasets import fetch_openml

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Flask says Hello!!!</p>"

@app.route("/ditto")
def ditto():
    soup = BeautifulSoup("<p>Some<b>bad<i>HTML")
    print(soup.prettify())
    llm = ChatOpenAI()
    llm.invoke("how can langsmith help with testing?")
    res = requests.get("https://pokeapi.co/api/v2/pokemon/ditto")
    X_adult, y_adult = fetch_openml("adult", version=2, return_X_y=True)

    # Remove redundant and non-feature columns
    X_adult = X_adult.drop(["education-num", "fnlwgt"], axis="columns")
    X_adult.dtypes
    return res.text

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)