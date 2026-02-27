from pydantic_settings import BaseSettings
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

class Setting(BaseSettings):
    firebase_cred_path: str
    bigquery_cred_path: str
    bigquery_project_id: str
    bigquery_dataset: str
    bigquery_table: str

    model_config = {
        "env_file": str(ROOT_DIR / ".env"),  # explicit absolute path
        "env_file_encoding": "utf-8"
    }

settings = Setting()