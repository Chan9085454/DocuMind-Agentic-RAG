import time
import requests
from app.core.config import OLLAMA_MODEL


def ask_llm(prompt):
    start = time.time()

    try:
        print(f"Using model: {OLLAMA_MODEL}")

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=150,
        )

        elapsed = time.time() - start

        print(
            f"ask_llm: status={response.status_code}, "
            f"time={elapsed:.2f}s"
        )

        if response.status_code != 200:
            print("OLLAMA ERROR")
            print(response.text)
            return "Model failed to generate response."

        data = response.json()

        if "response" not in data:
            print("Invalid response:", data)
            return "No response generated."

        return data["response"]

    except requests.exceptions.Timeout:
        print("Timeout Error")
        return "LLM timeout."

    except requests.exceptions.ConnectionError:
        print("Ollama server not running")
        return "Ollama server is not running."

    except Exception as e:
        elapsed = time.time() - start
        print(
            f"ask_llm error: {e} "
            f"(time={elapsed:.2f}s)"
        )
        return "Unexpected LLM error."