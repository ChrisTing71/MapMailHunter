from search_map import search_places
from fetch_email import fetch_emails_from_website
from save_result import save_results
import time

def collect_data(keyword, location_text):
    stores = search_places(keyword, location_text)
    result = {}
    for store in stores:
        name = store.get("name")
        website = store.get("website")
        emails = fetch_emails_from_website(website)
        result[name] = {
            "website": website,
            "emails": emails
        }
        time.sleep(1)  # 保護 API
    return result

if __name__ == "__main__":
    keyword = input("請輸入搜尋關鍵字（例如 咖啡店）: ")
    location = input("請輸入地點（例如 美國 亞利桑那）: ")
    data = collect_data(keyword, location)
    save_results(data)