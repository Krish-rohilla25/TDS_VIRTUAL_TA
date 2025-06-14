# TDS Virtual Teaching Assistant

This project is a virtual teaching assistant built for the Tools in Data Science (TDS) course offered by IIT Madras as part of the BS in Data Science and Applications program. It is designed to automatically answer student questions using the course content and Discourse forum posts.

The project was built as part of the TDS Project 1 assignment for the May 2025 batch.

## Overview

The backend is built using FastAPI and uses TF-IDF-based semantic search to retrieve the most relevant responses from:

- Course content from the official TDS Jan 2025 website (as on 15 April 2025)
- Discourse forum posts from the TDS Knowledge Base (1 Jan – 14 Apr 2025)

Users can ask any question via a POST request to the API and receive a concise answer, with matched sources and context.

## Features

- Accepts a student question as a POST request
- Searches both course content and Discourse posts
- Uses TF-IDF vectorization and cosine similarity
- Returns top matches with title, snippet, and source URL
- Supports Markdown-formatted responses

## API Usage

### Endpoint

```
POST /ask
```

### Request Body

```json
{
  "question": "How does SQLite work?"
}
```

### Response Format

```json
{
  "answer": "SQLite is a relational database used to store structured data...",
  "sources": [
    {
      "source": "course",
      "title": "Database: SQLite",
      "url": "https://tds.s-anand.net/#/../sqlite",
      "snippet": "Relational databases are used to store data in a structured way..."
    },
    {
      "source": "discourse",
      "title": "GA3 Discussion",
      "url": "https://discourse.onlinedegree.iitm.ac.in/t/ga3-question/123456/2",
      "snippet": "You can use SQLite to run queries from the command line..."
    }
  ],
  "sources_markdown": "- [Database: SQLite](https://tds.s-anand.net/#/../sqlite) (course)

  Relational databases are used to store data...

- [GA3 Discussion](https://discourse.onlinedegree.iitm.ac.in/t/ga3-question/123456/2) (discourse)

  You can use SQLite to run queries..."
}
```

## Folder Structure

```
tds_virtual_ta/
├── app/
│   ├── main.py
│   ├── tds_course_lessons.json
│   ├── tds_posts.json
│   └── utils/
│       ├── course_scraper.py
│       ├── discourse_scraper.py
│       └── answer_generator.py
├── requirements.txt
├── README.md
└── LICENSE
```

## Setup Instructions

1. Clone the repository and navigate to the project folder.

2. (Optional) Create and activate a virtual environment.

3. Install dependencies:

```
pip install -r requirements.txt
```

4. Run the application:

```
uvicorn app.main:app --reload
```

5. Visit Swagger UI to test:

```
http://127.0.0.1:8000/docs
```

## Deployment

This application is designed to run as a serverless FastAPI backend and can be deployed on platforms like Vercel or Render. It uses pre-scraped data and does not require a database or persistent storage.

## License

This project is licensed under the MIT License. See the LICENSE file for full details.
