import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()

COOKIES = {
    "_forum_session": os.getenv("DISCOURSE_SESSION"),
    "_t": os.getenv("DISCOURSE_TOKEN")
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Referer": "https://discourse.onlinedegree.iitm.ac.in/",
    "Origin": "https://discourse.onlinedegree.iitm.ac.in"
}

BASE_URL = "https://discourse.onlinedegree.iitm.ac.in"
CATEGORY_ID = 34
CATEGORY_JSON_URL = f"{BASE_URL}/c/courses/tds-kb/{CATEGORY_ID}.json"

#  Date filter range
START_DATE = datetime.strptime("2025-01-01", "%Y-%m-%d")
END_DATE = datetime.strptime("2025-04-14", "%Y-%m-%d")

def within_date_range(post_date_str):
    try:
        post_date = datetime.strptime(post_date_str[:10], "%Y-%m-%d")
        return START_DATE <= post_date <= END_DATE
    except:
        return False

def scrape_posts():
    print(" Fetching topic list...")
    try:
        resp = requests.get(CATEGORY_JSON_URL, headers=HEADERS, cookies=COOKIES)
        resp.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f" Failed to fetch topics: {e}")
        return

    topics = resp.json().get("topic_list", {}).get("topics", [])
    results = []

    for topic in topics:
        topic_id = topic["id"]
        topic_slug = topic["slug"]
        topic_url = f"{BASE_URL}/t/{topic_slug}/{topic_id}.json"

        topic_resp = requests.get(topic_url, headers=HEADERS, cookies=COOKIES)
        if topic_resp.status_code != 200:
            print(f"⚠️ Skipping topic {topic_id}, status {topic_resp.status_code}")
            continue

        topic_data = topic_resp.json()

        for post in topic_data.get("post_stream", {}).get("posts", []):
            created_at = post.get("created_at", "")
            if within_date_range(created_at):
                results.append({
                    "topic_title": topic_data.get("title"),
                    "post_number": post["post_number"],
                    "username": post["username"],
                    "created_at": created_at,
                    "cooked": BeautifulSoup(post["cooked"], "html.parser").get_text()
                })

    print(f"Scraped {len(results)} posts from TDS between Jan–Apr 2025.")
    with open("tds_posts.json", "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    scrape_posts()
