from playwright.sync_api import sync_playwright
import time

BASE_URL = "https://tds.s-anand.net/#"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://tds.s-anand.net/#/2025-01/")
    page.wait_for_timeout(5000)  # wait for JS to load

    all_links = page.locator("a").all()
    lesson_urls = []

    for link in all_links:
        try:
            href = link.get_attribute("href")
            text = link.inner_text().strip()

            if href and href.startswith("#/../") and text:
                # Normalize relative path
                full_url = BASE_URL + href[1:]  # remove leading #
                lesson_urls.append((text, full_url))
        except:
            continue

    print(f"✅ Found {len(lesson_urls)} lessons...")

    results = []

    for title, url in lesson_urls:
        try:
            page.goto(url)
            page.wait_for_timeout(2000)

            content = page.locator("main").inner_text(timeout=5000)
            results.append({
                "title": title,
                "url": url,
                "content": content
            })
            print(f"✅ Scraped: {title}")
        except Exception as e:
            print(f"⚠️ Failed to scrape {title}: {e}")
            continue

    browser.close()

# Save or print
import json
with open("tds_course_lessons.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print("✅ Done. Data saved to tds_course_lessons.json")
