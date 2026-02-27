from google.cloud import bigquery
from google.oauth2 import service_account
from core.config import settings

def get_bq_client():
    creds = service_account.Credentials.from_service_account_file(
        settings.bigquery_cred_path
    )
    return bigquery.Client(project=settings.bigquery_porject_id, credentials=creds)


def insert_articles(articles: list[dict]) -> dict:
    client = get_bq_client()
    table_id = f"{settings.bigquery_porject_id}.{settings.bigquery_dataset}.{settings.bigquery_table}"

    errors = client.insert_rows_json(table_id, articles)

    if errors:
        return {"code": 500, "status": "failed", "errors": errors }
    return {"code": 200, "status": "success", "inserted": len(articles)}

