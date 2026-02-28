from google.cloud import bigquery
from google.oauth2 import service_account
from core.config import settings
import json
from vertexai.language_models import TextEmbeddingModel
import vertexai
from io import StringIO

vertexai.init(project=f"{settings.bigquery_project_id}", location=settings.location)

def generate_embedding(text: str) -> list[float]:
    creds = service_account.Credentials.from_service_account_file(
        settings.bigquery_cred_path,
        scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )
    vertexai.init(
        project=settings.bigquery_project_id,
        location=settings.location,
        credentials=creds 
    )
    model = TextEmbeddingModel.from_pretrained("text-embedding-004")
    embeddings = model.get_embeddings([text])
    return embeddings[0].values


def flatten_article(article: dict) -> dict:
    text_for_embedding = " ".join(filter(None, [
        article.get("title"),                              
        article.get("summary", {}).get("summary"),         
        article.get("description"),                        
    ]))

    return {
        "articleId": article.get("articleId"),
        "title": article.get("title"),
        "description": article.get("description"),
        "content": article.get("content"),
        "author": article.get("author"),
        "article_url": article.get("url"),
        "urltoimage": article.get("urlToImage"),
        "country": article.get("country"),
        "publishedat": article.get("publishedAt"),

        # Flatten source
        "source_type": article.get("source", {}).get("name"),

        # Flatten summary
        "category": article.get("summary", {}).get("category"),
        "summary": article.get("summary", {}).get("summary"),
        "embedding": generate_embedding(text_for_embedding)
    }

def get_bq_client():
    creds = service_account.Credentials.from_service_account_file(
        settings.bigquery_cred_path
    )
    return bigquery.Client(project=settings.bigquery_project_id, credentials=creds)


def insert_articles(articles: list[dict]) -> dict:
    client = get_bq_client()
    table_id = f"{settings.bigquery_project_id}.{settings.bigquery_dataset}.{settings.bigquery_table}"

    # flattened = [flatten_article(a) for a in [articles]]
    # errors = client.insert_rows_json(table_id, flattened)

    # ✅ Flatten + embed each article
    flattened = [flatten_article(a) for a in [articles]]

    json_data = "\n".join([json.dumps(a) for a in flattened])
    data_file = StringIO(json_data)

    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
        autodetect=False
    )

    job = client.load_table_from_file(data_file, table_id, job_config=job_config)
    job.result()  

    if job.errors:
        return {"status": "failed", "errors": job.errors}
    return {"status": "success", "inserted": len(flattened)}

