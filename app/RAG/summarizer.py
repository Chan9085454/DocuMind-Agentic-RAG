import time
from app.ingestion.embedder import get_embeddings
from app.vectorstore.chroma_store import search
from app.RAG.llm_utils import ask_llm


def summarize_documents(question, top_k=10):
    """
    Summarize documents relevant to the question.
    """
    t0 = time.time()
    print(f"summarize_documents: received question (len={len(question)})")

    t1 = time.time()
    q_embedding = get_embeddings([question])[0]
    print(f"summarize_documents: embedding time={(time.time()-t1):.2f}s")

    t2 = time.time()
    results = search(q_embedding, n_results=top_k)
    print(f"summarize_documents: search time={(time.time()-t2):.2f}s results_keys={list(results.keys())}")

    
    docs = []
    try:
        docs = results.get("documents", [[]])[0]
    except Exception:
        docs = []

    if not docs:
        return "No relevant documents found to summarize."

    context = "\n".join(docs)

    prompt = f"""
    Summarize the following text in a concise manner.

    Text:
    {context}

    Summary:
    """

    print(f"summarize_documents: building prompt (context_len={len(context)})")
    summary = ask_llm(prompt)
    print(f"summarize_documents: total_time={(time.time()-t0):.2f}s")
    return summary