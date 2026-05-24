import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app/RAG')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app/core')))

from qa_chain import answer_question

if __name__ == "__main__":
    question = "What is RNN?"
    try:
        print("Calling answer_question...")
        result = answer_question(question)
        print("Result:", result)
    except Exception as e:
        print("Error:", repr(e))
