from sentence_transformers import SentenceTransformer
from app.core.config import EMBEDDING_MODEL

model = SentenceTransformer(EMBEDDING_MODEL)

def get_embeddings(texts):
    return model.encode(texts).tolist()