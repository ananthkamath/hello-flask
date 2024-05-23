from flask import Flask, json
import requests

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Flask says Hello!!!</p>"

@app.route("/ditto")
def ditto():
    res = requests.get("https://pokeapi.co/api/v2/pokemon/ditto")
    return res.text
