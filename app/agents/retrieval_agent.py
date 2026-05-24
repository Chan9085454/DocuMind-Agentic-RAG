class RetrievalAgent:
    def __init__(self, vectorstore):
        self.vectorstore = vectorstore

    def run(self, query: str):
        docs = self.vectorstore.similarity_search(query, k=3)

        return {
            "documents": docs
        }