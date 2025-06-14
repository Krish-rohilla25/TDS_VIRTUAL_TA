import json
import os

DISCOURSE_DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "tds_posts.json")

def load_discourse_data():
    with open(DISCOURSE_DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)
