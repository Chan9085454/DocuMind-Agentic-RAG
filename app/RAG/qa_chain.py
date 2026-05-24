import time
from app.ingestion.embedder import get_embeddings
from app.vectorstore.chroma_store import search
from app.RAG.llm_utils import ask_llm
from app.RAG.summarizer import summarize_documents

from app.agents.tool_agent import ToolAgent
from app.agents.planner_agent import PlannerAgent
from app.agents.memory import Memory

tool = ToolAgent()
planner = PlannerAgent()
memory = Memory()


def is_low_confidence(docs):
    if not docs or len(docs) < 2:
        return True
    total_length = sum(len(doc) for doc in docs if isinstance(doc, str))
    return total_length < 200


def answer_question(question):
    t0 = time.time()
    print(f"Question received: {question}")

    # Step 1: Planner decides route
    plan = planner.run(question)
    route = plan.get("route", "rag")

    print(f"Planner decision: {route}")

    # Step 2: Memory context
    history = memory.get_context()

    # Step 3: Summarization shortcut
    if "summarize" in question.lower():
        answer = summarize_documents(question)
        memory.add(question, answer)
        return answer

    # ROUTE 1: LLM ONLY
    if route == "llm":
        answer = tool.run(question)["tool_result"]
        memory.add(question, answer)
        return answer

    # Step 4: RAG pipeline
    q_embedding = get_embeddings([question])[0]
    results = search(q_embedding)

    try:
        docs = results.get("documents", [[]])[0]
    except:
        docs = []

    context = "\n".join(docs)

    # ROUTE 2: HYBRID (RAG + LLM)
    if route == "hybrid":
        print("Using HYBRID mode")

        rag_part = context[:1500]

        hybrid_prompt = f"""
        Use both document context and your knowledge.

        Chat History:
        {history}

        Context:
        {rag_part}

        Question:
        {question}
        """

        answer = ask_llm(hybrid_prompt)
        memory.add(question, answer)
        return answer

    # ROUTE 3: RAG (default)
    if is_low_confidence(docs):
        print("Low confidence → fallback to ToolAgent")
        answer = tool.run(question)["tool_result"]
        memory.add(question, answer)
        return answer

    
    snippets = []
    seen = set()

    for doc in docs:
        text = " ".join(str(doc).split())
        if not text or text in seen:
            continue

        seen.add(text)
        snippets.append(text[:500])

        if len(snippets) >= 3:
            break

    if not snippets:
        answer = tool.run(question)["tool_result"]
        memory.add(question, answer)
        return answer

    context_text = "\n\n".join(snippets)

    final_prompt = f"""
    Use ONLY the document context to answer the question.
    If the answer can be quoted directly from the context, preserve the exact wording or phrasing.
    Do not add examples, use cases, or any information not present in the document.
    If the answer is not found in the context, respond with exactly:
    Answer not found in document.

    Chat History:
    {history}

    Context:
    {context_text}

    Question:
    {question}
    """

    answer = ask_llm(final_prompt)

    # fallback if failed
    if not answer or "outside" in answer.lower():
        answer = tool.run(question, context_text)["tool_result"]

    memory.add(question, answer)

    print(f"Total time: {time.time()-t0:.2f}s")

    return answer