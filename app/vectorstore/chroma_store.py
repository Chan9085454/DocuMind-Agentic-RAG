import chromadb
from chromadb.config import Settings
from app.core.config import VECTOR_DB_DIR
from app.ingestion.embedder import get_embeddings


client = chromadb.Client(Settings(persist_directory=VECTOR_DB_DIR))
collection = client.get_or_create_collection(name="documind")


def add_to_vectorstore(texts, embeddings, metadatas, ids):
    collection.add(
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids,
    )


def search(query_embedding, n_results=3):
    res = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        include=["documents", "metadatas", "distances"]  
    )
    return res


class _SimpleDoc:
    def __init__(self, content, metadata=None):
        self.page_content = content
        self.metadata = metadata


class _VectorStoreWrapper:
    def __init__(self, collection):
        self.collection = collection

    def similarity_search(self, query: str, k: int = 5):
        emb = get_embeddings([query])[0]

        
        res = self.collection.query(
            query_embeddings=[emb],
            n_results=k,
            include=["documents", "metadatas", "distances"]
        )

        documents = res.get("documents", [])
        metadatas = res.get("metadatas", [])
        distances = res.get("distances", [])

        # Handle nested lists
        doc_list = documents[0] if documents and isinstance(documents[0], list) else documents
        meta_list = metadatas[0] if metadatas and isinstance(metadatas[0], list) else metadatas
        dist_list = distances[0] if distances and isinstance(distances[0], list) else distances

        results = []
        for i, content in enumerate(doc_list):
            meta = meta_list[i] if i < len(meta_list) else None
            dist = dist_list[i] if i < len(dist_list) else None

            doc = _SimpleDoc(content, meta)

           
            doc.score = dist

            results.append(doc)

        return results


def get_vectorstore():
    return _VectorStoreWrapper(collection)