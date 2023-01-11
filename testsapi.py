import json
import requests


BASE_URL = "http://127.0.0.1:5000/"

response = requests.get(BASE_URL)
books = response.json()

with open("src/fixtures/books.json", "w") as f:
    json.dump(books, f, indent=2)
