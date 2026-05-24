from app.agents.planner_agent import PlannerAgent
from app.agents.retrieval_agent import RetrievalAgent
from app.agents.reasoning_agent import ReasoningAgent
from app.agents.response_agent import ResponseAgent
from app.agents.tool_agent import ToolAgent


class AgentManager:
    def __init__(self, vectorstore):
        # Accept an LLM instance and a vectorstore
        self.planner = PlannerAgent()
        self.retriever = RetrievalAgent(vectorstore)
        self.reasoner = ReasoningAgent()
        self.responder = ResponseAgent()
        self.tool = ToolAgent()

    def run(self, query: str):
        print("\n--- AGENT START ---")

        
        plan = self.planner.run(query)
        route = plan.get("route", "rag")

        print("Planner route:", route)

        docs = []
        reasoning_output = ""
        tool_output = None

       
        if route == "rag":
            retrieval_output = self.retriever.run(query)
            docs = retrieval_output.get("documents", [])

            print("Docs:", len(docs))

            if docs:
                reasoning_output = self.reasoner.run(query, docs)["answer"]

        
        elif route == "hybrid":
            retrieval_output = self.retriever.run(query)
            docs = retrieval_output.get("documents", [])

            context = "\n".join([doc.page_content for doc in docs]) if docs else ""

            tool_output = self.tool.run(query, context)["tool_result"]

       
        final_answer = self.responder.run(
            query,
            reasoning_output,
            tool_output
        )

        
        if not final_answer or str(final_answer).strip() == "":
            final_answer = "No answer generated."

        print("Final Answer:", final_answer)
        print("--- AGENT END ---\n")

        return final_answer