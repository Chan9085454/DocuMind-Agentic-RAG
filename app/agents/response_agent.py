from app.core.llm import get_llm

class ResponseAgent:
    def __init__(self):
        self.llm = get_llm()

    def run(self, query, reasoning_output, tool_output=None):

       
        if reasoning_output and str(reasoning_output).strip():
            return str(reasoning_output)

        
        if tool_output:
            return str(tool_output)

        
        return "No relevant answer found."