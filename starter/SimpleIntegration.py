from dotenv import load_dotenv
from google import genai
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("API_KEY")
)


response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Explain RAG in 3 sentences"
)



response_format = "\n===================================================\n"


response_format
print(response.text)
response_format