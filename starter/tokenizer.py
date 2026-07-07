from transformers  import AutoTokenizer
from dotenv import load_dotenv
from google import genai
from google.genai import types
import os

load_dotenv()

os.environ["HF_TOKEN"] = os.getenv("HF_TOKEN")
tokenizer = AutoTokenizer.from_pretrained("gemini-2.5-flash")
client = genai.Client(api_key=os.getenv("API_KEY"))


tokenizer("Hey There! How are you doing today?")