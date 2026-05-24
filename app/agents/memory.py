class Memory:
    def __init__(self):
        self.chat_history = []

    def add(self, user, assistant):
        self.chat_history.append({
            "user": user,
            "assistant": assistant
        })

    def get_context(self):
        history_text = ""
        for item in self.chat_history[-5:]:  # last 5 messages
            history_text += f"User: {item['user']}\nAssistant: {item['assistant']}\n"
        return history_text