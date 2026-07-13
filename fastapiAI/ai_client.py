from dotenv import load_dotenv
from google import genai
from google.genai import types
import os   

load_dotenv()
client = genai.Client(api_key=os.getenv("API_KEY"))



response_model_text = "gemini-2.5-flash"


def generate_text(prompt):
    response = client.models.generate_content(
        model=response_model_text,
        config=types.GenerateContentConfig(max_output_tokens=100),
        contents=[prompt]
    )
    return response.text
