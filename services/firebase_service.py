import firebase_admin
from firebase_admin import credentials, firestore
from core.config import settings

def get_firebase_client():
    if not firebase_admin._apps:
        cred = credentials.Certificate(settings.firebase_cred_path)
        firebase_admin.initialize_app(cred)
    return firestore.client()


def fetch_articles(collection: str = "articles") -> list[dict]:
    db = get_firebase_client()
    docs = db.collection(collection).stream()
    return [{"id": doc.id, **doc.to_dict()} for doc in docs]
