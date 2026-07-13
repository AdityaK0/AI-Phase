from dotenv import load_dotenv
from google import genai
import os

load_dotenv()
client = genai.Client(api_key=os.getenv("API_KEY"))


result = client.models.embed_content(
    model="gemini-embedding-001",
    contents=["What is a neural network?"]
)


vector = result.embeddings[0].values
print(f"Vector length: {vector}")
print(f"Dimensions: {len(vector)}")
print(f"First 5 values: {vector[:5]}")