from flask import Flask, request, jsonify, render_template
import requests
import os

app = Flask(__name__)
API_KEY = os.environ.get("API_KEY")
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

CATEGORIES = ["Cafe", "Boba", "Pizza", "Burgers", "Chinese", "Japanese", "Mexican", "Indian", "Italian"]

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        zip_code = request.form.get("zip")
        category = request.form.get("category")

        if zip_code and category:
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
        else:
           
            return render_template("index.html", error="Please provide both zip and category.")
    else:
       
        return render_template("index.html")

