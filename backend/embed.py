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

# 1. Load dataset
with open("../data/bns_data.json", "r", encoding="utf-8") as f:
    dataset = json.load(f)

# 2. Create embeddings
embeddings = []
for entry in dataset:
    text = f"{entry['section_title']}: {entry['description']}"
    emb = genai.embed_content(
        model="models/text-embedding-004",
        content=text
    )["embedding"]
    embeddings.append(np.array(emb, dtype="float32"))

embeddings = np.vstack(embeddings)

# 3. Create FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# 4. Save index
faiss.write_index(index, "../data/bns_index.faiss")

print(f"✅ Embedded {len(dataset)} sections into FAISS index.")
