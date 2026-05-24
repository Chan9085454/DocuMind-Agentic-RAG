from app.core.llm import get_llm

class ToolAgent:
    def __init__(self):
        self.llm = get_llm()

    def run(self, query: str, context: str = None):
       
        if context:
            prompt = f"""
            You are an AI assistant.

            Use the given context to answer the question.
            If the context is not sufficient, you can use your own knowledge.
            If you still don't know, say "I don't know".

            Context:
            {context}

            Question:
            {query}
            """
        else:
            # Fallback when no documents found
            prompt = f"""
            You are an AI assistant.

            Answer the question using your general knowledge.
            If you are not sure, say "I don't know".

            Question:
            {query}
            """

        response = self.llm.invoke(prompt)

        return {
            "tool_result": response
        }