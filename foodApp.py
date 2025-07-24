from flask import Flask, request, jsonify
import requests
from dotenv import dotenv_values
import os

secrets = dotenv_values(".env")

app = Flask(__name__)
API_KEY = os.environ.get("API_KEY")
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

CATEGORIES = ["Cafe", "Boba", "Pizza", "Burgers", "Chinese", "Japanese", "Mexican", "Indian", "Italian"]

@app.route("/search", methods=["GET"])
def search():
    zip_code = request.args.get("zip")
    category = request.args.get("category")

    if not zip_code or not category:
        return jsonify({"error": "Missing zip or category"}), 400

    url = "https://api.yelp.com/v3/businesses/search"
    params = {
        "term": category,
        "location": zip_code,
        "limit": 5,
        "sort_by": "rating"
    }

    response = requests.get(url, headers=HEADERS, params=params)
    data = response.json()

    if response.status_code != 200:
        return jsonify({"error": "Yelp API failed", "details": data}), 500

    businesses = data.get("businesses", [])
    results = [{
        "name": b["name"],
        "rating": b["rating"],
        "address": ", ".join(b["location"]["display_address"])
    } for b in businesses]

    return jsonify(results)
