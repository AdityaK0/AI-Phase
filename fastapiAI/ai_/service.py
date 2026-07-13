

from ai_client import generate_text

class AIService:
    def __init__(self):
        pass

    def process_request(self, request_data):
        prompt = request_data.get("prompt", "")
        # Implement your AI processing logic here
        response_text = generate_text(prompt)
        response_data = {"result": response_text}
        return response_data