from dotenv import load_dotenv
from google import genai
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
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )
    return np.array(result.embeddings[0].values)

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

print("Embedding documents...")
doc_embeddings = [get_embedding(doc) for doc in documents]

query = input("Ask a question: ")
query_embedding = get_embedding(query)

similarities = [cosine_similarity(query_embedding, doc_emb) for doc_emb in doc_embeddings]
best_idx = np.argmax(similarities)

print(f"\nMost relevant chunk (score: {similarities[best_idx]:.3f}):")
print(documents[best_idx])

# Also print all scores so you can see the gap
print("\nAll scores:")
for i, score in enumerate(similarities):
    print(f"  {score:.3f} — {documents[i][:50]}...")
