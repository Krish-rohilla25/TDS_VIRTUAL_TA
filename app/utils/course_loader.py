import json
import os

COURSE_DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "tds_course_lessons.json")

def load_course_data():
    with open(COURSE_DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)
