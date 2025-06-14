import json
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

COURSE_PATH = os.path.join(os.path.dirname(__file__), "..", "tds_course_lessons.json")
DISCOURSE_PATH = os.path.join(os.path.dirname(__file__), "..", "tds_posts.json")

def load_data():
    with open(COURSE_PATH, "r", encoding="utf-8") as f:
        course_data = json.load(f)

    with open(DISCOURSE_PATH, "r", encoding="utf-8") as f:
        discourse_data = json.load(f)

    all_texts = []
    sources = []

    # Course content
    for item in course_data:
        content = item.get("content", "")
        title = item.get("title", "")
        url = item.get("url", "")
        all_texts.append(content)
        sources.append({
            "type": "course",
            "title": title,
            "url": url,
            "text": content
        })

    # Discourse posts
    for post in discourse_data:
        content = post.get("cooked", "")
        topic = post.get("topic_title", "")
        post_number = post.get("post_number", 1)
        topic_id = post.get("topic_id", None)

        if topic_id:
            slug = topic.lower().replace(" ", "-")
            url = f"https://discourse.onlinedegree.iitm.ac.in/t/{slug}/{topic_id}/{post_number}"
        else:
            url = ""

        all_texts.append(content)
        sources.append({
            "type": "discourse",
            "title": topic,
            "url": url,
            "text": content
        })

    return all_texts, sources


def clean_snippet(text: str, max_lines: int = 10, max_length: int = 400) -> str:
    lines = text.strip().splitlines()

    # Skip TOC or repeated heading blocks
    for i, line in enumerate(lines):
        line_lower = line.strip().lower()
        if any(keyword in line_lower for keyword in [
            "vercel", "uvicorn", "deployment", "main.py", "fastapi", "api", "run", "requirement", "serverless"
        ]):
            lines = lines[i:]
            break

    # Remove generic or noisy lines
    lines = [
        line for line in lines
        if line.strip()
        and not line.strip().lower().startswith("tools in data science")
        and not line.strip().isdigit()
    ]

    snippet = " ".join(lines[:max_lines])
    return snippet[:max_length] + ("..." if len(snippet) > max_length else "")




def generate_answer(query: str, top_k: int = 3):
    all_texts, sources = load_data()

    vectorizer = TfidfVectorizer(stop_words='english').fit_transform([query] + all_texts)
    similarity = cosine_similarity(vectorizer[0:1], vectorizer[1:]).flatten()

    top_indices = similarity.argsort()[-top_k:][::-1]
    results = []

    for idx in top_indices:
        score = similarity[idx]
        if score < 0.05:
            continue
        item = sources[idx]
        results.append({
            "source": item["type"],
            "title": item["title"],
            "url": item["url"],
            "snippet": clean_snippet(item["text"])
        })

    if not results:
        return "Sorry, I couldn’t find a relevant answer.", []

    return results[0]["snippet"], results
