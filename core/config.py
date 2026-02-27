from pydantic_settings import BaseSettings

class Setting(BaseSettings):
    firebase_cred_path: str
    bigquery_cred_path: str
    bigquery_porject_id: str
    bigquery_dataset: str
    bigquery_table: str

    class config:
        env_file = ".env"

settings = Setting()