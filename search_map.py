import googlemaps
import time
from dotenv import load_dotenv
import os
import requests

load_dotenv(dotenv_path=".env")
API_KEY = os.getenv("API_KEY")

def search_places(keyword, location_text):
    query = f"{keyword} {location_text}"
    url = (
        f"https://maps.googleapis.com/maps/api/place/textsearch/json"
        f"?query={query}&key={API_KEY}"
    )
    results = []
    while url:
        print(f"請求: {url}")
        resp = requests.get(url)
        data = resp.json()
        results.extend(parse_results(data))
        next_page_token = data.get("next_page_token")
        if next_page_token:
            print("有下一頁，等 token 有效...")
            time.sleep(2)
            url = (
                f"https://maps.googleapis.com/maps/api/place/textsearch/json"
                f"?pagetoken={next_page_token}&key={API_KEY}"
            )
        else:
            url = None
    return results

def parse_results(data):
    output = []
    for r in data.get("results", []):
        place_id = r.get("place_id")
        name = r.get("name")
        website = fetch_website(place_id)
        output.append({
            "name": name,
            "website": website
        })
    return output

def fetch_website(place_id):
    url = (
        f"https://maps.googleapis.com/maps/api/place/details/json"
        f"?place_id={place_id}&fields=website&key={API_KEY}"
    )
    resp = requests.get(url)
    data = resp.json()
    return data.get("result", {}).get("website")
