from fastapi import APIRouter
from app.vectorstore.chroma_store import get_vectorstore
from app.agents.agent_manager import AgentManager

router = APIRouter()


@router.post("/chat")
def chat(query: str):
    try:
        vectorstore = get_vectorstore()
        agent = AgentManager(vectorstore)

        response = agent.run(query)

        if not response or str(response).strip() == "":
            response = "No answer generated."

        return {"answer": response}

    except Exception as e:
        print("CHAT ERROR:", e)
        return {"answer": "Something went wrong. Please try again."}