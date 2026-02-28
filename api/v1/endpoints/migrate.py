from fastapi import APIRouter, HTTPException
from services.firebase_service import fetch_articles
from services.bigquery_service import insert_articles
from pydantic import BaseModel

router = APIRouter()

class MigrateRequest(BaseModel):
    collection: str = "articles"

@router.post("/migrate")
async def migrate_articles(request: MigrateRequest):
    try:
        articles = fetch_articles(request.collection)
        if not articles:
            raise HTTPException(status_code=404, detail="No articles found in firebase")
        
        result =  insert_articles(articles[10:15])

        return {
            "msg": "Migration compelted",
            "total_fetched": len(articles),
            **result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/preview")
async def preview_articles(collection: str = "inbits_collection/us/articles", limit: int = 5):
    articles = fetch_articles(collection)
    return { "code": 200, "articles": articles[:limit], "total": len(articles)}