from dotenv import load_dotenv
from google import genai
from google.genai import types
import os
import numpy as np

load_dotenv()
client = genai.Client(api_key=os.getenv("API_KEY"))

documents = [
    "FastAPI is a modern Python web framework for building APIs with async support.",
    "PostgreSQL is a powerful open-source relational database with ACID compliance.",
    "RAG stands for Retrieval-Augmented Generation - it injects relevant context into LLM prompts.",
    "Docker containers package applications with their dependencies for consistent deployment.",
    "Embeddings convert text into numerical vectors that capture semantic meaning.",
]

def get_embedding(text):
    result = client.models.embed_content(model="gemini-embedding-001", contents=text)
    return np.array(result.embeddings[0].values)

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Pre-embed all documents once
print("Embedding documents...")
doc_embeddings = [get_embedding(doc) for doc in documents]

while True:
    query = input("\nYou: ")
    if query.lower() == "quit":
        break

    # Step 1: find the most relevant chunk
    query_embedding = get_embedding(query)
    similarities = [cosine_similarity(query_embedding, e) for e in doc_embeddings]
    best_idx = np.argmax(similarities)
    best_score = similarities[best_idx]

    # Step 2: relevance threshold
    if best_score < 0.5:
        print("AI: I don't have relevant information to answer that.")
        continue

    retrieved_chunk = documents[best_idx]
    print(f"[Retrieved: '{retrieved_chunk[:60]}...' (score: {best_score:.3f})]")

    # Step 3: send chunk + question to LLM
    prompt = f"""You are a helpful assistant. Use the context below to answer the question.
Keep your answer brief and based on the context provided.

Context: {retrieved_chunk}

Question: {query}"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction="You are a helpful assistant. Be concise."
        ),
        contents=prompt,
    )

    print(f"AI: {response.text}")
