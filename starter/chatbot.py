from dotenv import load_dotenv
from google import genai
from google.genai import types
import os


load_dotenv()


client = genai.Client(api_key=os.getenv("API_KEY"))

system_prompt = "You are a concise technical assistant. Answer in bullet points only"


chat_history = []
chat_request_reponse = []

while True:
    user_input = input("You: ")
    
    if user_input.lower() == "quit":
        break
    if user_input.lower() == "previous":
        print(chat_history[-1],"\n")
    
    chat_history.append(types.Content(role="user", parts=[types.Part(text=user_input)]))
    
    
    response = client.models.generate_content(
        model = "gemini-2.5-flash",
        config = types.GenerateContentConfig(system_instruction=system_prompt),
        contents=chat_history,
    )
    
    reply = response.text
    
    print(f"AI: {reply}\n")
    chat_request_reponse.append((user_input,reply))
    
    chat_history.append(types.Content(role="model",parts=[types.Part(text=reply)]))
    