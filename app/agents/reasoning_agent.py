from app.core.llm import get_llm

class ReasoningAgent:
    def __init__(self):
        self.llm = get_llm()

    def run(self, query: str, docs: list):

        if not docs:
            return {"answer": ""}

        context_sections = []
        for index, doc in enumerate(docs, start=1):
            text = str(doc.page_content).strip()
            if not text:
                continue
            context_sections.append(f"--- Document {index} ---\n{text}")

        context = "\n\n".join(context_sections)
        context = context[:4000]

        prompt = f"""
You are a document reasoning agent.

Use ONLY the information provided in the CONTEXT section below to answer the question.
If the answer is present in the context, preserve the exact wording from the source or reuse the same phrasing as closely as possible.
Do not add examples, applications, or any information not found in the document.
If the answer cannot be found in the context, respond with exactly:
Answer not found in document.

CONTEXT:
{context}

QUESTION:
{query}
"""

        response = self.llm.invoke(prompt)
        answer = str(response).strip()

        return {
            "answer": answer
        }