from fastapi import FastAPI
from api.v1.endpoints.migrate import router as migrate_router

app = FastAPI(
    title= "Article Migrator",
    description="Migrate articles from Firebase to BigQuery",
    version="1.0.0"
)

app.include_router(migrate_router, prefix="/api/v1", tags=["Migration"])

@app.get("/health")
def health():
    return {"status": "App is working"}