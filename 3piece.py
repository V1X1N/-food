import requests

API_KEY = "6HcVgm5PhjQ4Pr6ERrnSkcEn-mLjxEs7Oo4c89PW9QR1JSkHP5QlGoNa6J1aD1xBueFGgtstGIqY1yhjrhzvsMfaadGE-vkWMmKp92UCYWuQ-Tbz2slsmj8RD1l9aHYx"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}
zip_code = "10001"  

CATEGORIES = [
    "Cafe",
    "Boba",
    "Pizza",
    "Burgers",
    "Chinese",
    "Japanese",
    "Mexican",
    "Indian",
    "Italian",
]

def search_yelp(zip_code):
    results = {}
    for category in CATEGORIES:
        params = {
            'term': category,
            'location': zip_code,
            'limit': 10,
            'sort_by': 'rating'
        }

response = requests.get("https://api.yelp.com/v3/businesses/search", headers=HEADERS, params=params)
print("Status:", response.status_code)
data = response.json()


businesses = data.get('businesses', [])
print("\nTop Pizza Spots:")
for b in businesses:
    print(f"{b['name']} - Rating: {b['rating']}")