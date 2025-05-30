class MemoryKeeper:
    def __init__(self):
        self.history = []

    def remember(self, user_input, response):
        self.history.append((user_input, response))

    def get_context(self):
        return "\n".join([f"Q: {q}\nA: {a}" for q, a in self.history])