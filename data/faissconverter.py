import json
import numpy as np
import faiss
import google.generativeai as genai
import os # Make sure to add this at the top of the file

# Configure Gemini
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY environment variable not set.")
genai.configure(api_key=api_key)

# Load dataset (use raw string or double backslashes)
with open("bnss_data.json", "r", encoding="utf-8") as f:
    dataset = json.load(f)

# Create embeddings
embeddings = []
for entry in dataset:
    text = f"{entry['section_title']}: {entry['description']}"
    emb = genai.embed_content(
        model="models/text-embedding-004",
        content=text
    )["embedding"]
    embeddings.append(np.array(emb, dtype="float32"))

embeddings = np.vstack(embeddings)

# Create FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# Save FAISS index (again raw string path is safer)
faiss.write_index(index, "bnss_index.faiss")

print(f"✅ Converted {len(dataset)} BNSS sections into FAISS index.")
