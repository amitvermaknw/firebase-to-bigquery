# 🔥➡️ Firebase to BigQuery Article Migrator

A FastAPI-powered service to migrate articles from **Firebase Firestore** to **Google BigQuery**.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the App](#running-the-app)
- [API Endpoints](#api-endpoints)
- [Troubleshooting](#troubleshooting)

---

## Overview

This service provides a REST API to:
- Fetch articles from a **Firebase Firestore** collection
- Validate and transform the data using **Pydantic schemas**
- Insert articles into a **Google BigQuery** table

---

## Project Structure

```
firebase-to-bigquery/
├── main.py                        # FastAPI app entry point
├── .env                           # Environment variables (do not commit)
├── requirements.txt
├── core/
│   └── config.py                  # Pydantic settings loader
├── api/
│   └── v1/
│       └── endpoints/
│           └── migrate.py         # Migration API routes
├── services/
│   ├── firebase_service.py        # Fetch articles from Firestore
│   └── bigquery_service.py        # Insert articles into BigQuery
├── schemas/
│   └── article.py                 # Pydantic article model
└── credentials/
    ├── firebase_creds.json        # Firebase service account key
    └── bigquery_creds.json        # BigQuery service account key
```

---

## Prerequisites

- Python 3.12+
- A **Firebase** project with Firestore enabled
- A **Google Cloud** project with BigQuery enabled
- Service account JSON keys for both Firebase and BigQuery

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/firebase-to-bigquery.git
cd firebase-to-bigquery
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate        # macOS/Linux
.venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install fastapi uvicorn firebase-admin google-cloud-bigquery pydantic-settings python-dotenv
```

Or using a requirements file:

```bash
pip install -r requirements.txt
```

---

## Configuration

### 1. Add credentials

Place your service account JSON files inside the `credentials/` folder:

```
credentials/
├── firebase_creds.json
└── bigquery_creds.json
```

### 2. Create a `.env` file in the project root

```env
FIREBASE_CRED_PATH=credentials/firebase_creds.json
BIGQUERY_CRED_PATH=credentials/bigquery_creds.json
BIGQUERY_PROJECT_ID=your-gcp-project-id
BIGQUERY_DATASET=articles_dataset
BIGQUERY_TABLE=articles
```

> ⚠️ Never commit `.env` or `credentials/` to version control. Add them to `.gitignore`.

### 3. `.gitignore` recommendation

```
.env
credentials/
.venv/
__pycache__/
```

---

## Running the App

```bash
uvicorn main:app --reload
```

The API will be available at: `http://localhost:8000`

Interactive docs: `http://localhost:8000/docs`

---

## API Endpoints

### `GET /health`
Check if the service is running.

**Response:**
```json
{ "status": "ok" }
```

---

### `GET /api/v1/preview?collection=articles&limit=5`
Preview articles fetched from Firestore without migrating.

| Parameter    | Type   | Default    | Description                        |
|-------------|--------|------------|------------------------------------|
| `collection` | string | `articles` | Firestore collection name          |
| `limit`      | int    | `5`        | Number of articles to preview      |

**Response:**
```json
{
  "articles": [...],
  "total": 42
}
```

---

### `POST /api/v1/migrate?collection=articles`
Migrate all articles from Firestore to BigQuery.

| Parameter    | Type   | Default    | Description               |
|-------------|--------|------------|---------------------------|
| `collection` | string | `articles` | Firestore collection name |

**Response:**
```json
{
  "message": "Migration complete",
  "total_fetched": 42,
  "status": "success",
  "inserted": 42
}
```

---

## Troubleshooting

| Error | Fix |
|-------|-----|
| `ValidationError: Field required` | Check your `.env` file exists in the root and all keys are correct |
| `Address already in use` | Run `kill -9 $(lsof -t -i:8000)` to free port 8000 |
| `A path prefix must start with '/'` | Ensure `prefix="/api/v1"` has a leading slash in `main.py` |
| `firebase_admin` not initialized | Ensure `firebase_creds.json` path is correct in `.env` |
| BigQuery insert errors | Verify your BigQuery table schema matches the article fields |

---

## Migration Flow

```
Firebase Firestore
       │
       ▼
  fetch_articles()          ← firebase_service.py
       │
       ▼
  Pydantic Validation       ← schemas/article.py
       │
       ▼
  insert_articles()         ← bigquery_service.py
       │
       ▼
  Google BigQuery Table
```
