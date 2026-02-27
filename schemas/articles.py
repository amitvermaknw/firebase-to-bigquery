from pydantic import BaseModel
from typing import Optional

class Article(BaseModel):
    articleId: str 
    content: Optional[str] = None
    description: Optional[str] = None 
    publishedat: Optional[str] = None 
    category: Optional[str] = None 
    summary: str 
    title: str 
    article_url: str 
    urltoimage: Optional[str] = None 
    embedding: float
    author: Optional[str] = None
    country: Optional[str] = None
    source_type: Optional[str] = None