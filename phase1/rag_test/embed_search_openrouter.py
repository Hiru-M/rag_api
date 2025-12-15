
import os
import argparse
import requests
import numpy as np
from scipy.spatial.distance import cdist
import sys
import time
from getpass import getpass  

# Config / Samples
EMBEDDING_MODEL = "openai/text-embedding-3-large"
samples = [
    "How to fix a leaking pipe in the kitchen",
    "Troubleshooting network connection issues",
    "Steps to bake a chocolate cake",
    "User manual for the AC unit model X200",
    "How to train a machine learning model",
    "Symptoms of a failing hard drive",
    "Guide to planting tomatoes in a pot",
    "How to change a flat bicycle tire",
    "Introduction to neural networks and embeddings",
    "Best practices for API authentication"
]


def parse_args():
    p = argparse.ArgumentParser(description="Embed 10 texts and find top-3 similar to a query using OpenRouter.")
    p.add_argument("--key", type=str, help="OpenRouter API key (one-shot).")
    p.add_argument("--query", type=str, default="How do I repair a pipe that is leaking under the sink?",
                   help="Query text to search for.")
    return p.parse_args()

def get_api_key_from_anywhere(cli_key=None):
    if cli_key:
        return cli_key.strip()

    env_key = os.getenv("OPENROUTER_API_KEY")
    if env_key:
        return env_key.strip()

    try:
        print("OpenRouter API key not found in args or environment.")
        print("Paste the key now. It will not be saved to disk.")
        # use getpass to avoid echoing on screen
        k = getpass("OpenRouter API key: ").strip()
        if k:
            return k
    except Exception:
        pass

    raise RuntimeError("No API key provided. Use --key, set OPENROUTER_API_KEY, or paste when prompted.")

def get_embedding(text, api_key, model=EMBEDDING_MODEL, max_retries=3, backoff=1.0):
    url = "https://openrouter.ai/api/v1/embeddings"
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {"model": model, "input": text}
    for attempt in range(max_retries):
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            emb = data["data"][0]["embedding"]
            return np.array(emb, dtype=float)
        except requests.exceptions.RequestException as e:
            print(f"Request error (attempt {attempt+1}/{max_retries}): {e}")
            time.sleep(backoff * (attempt+1))
    raise RuntimeError("Failed to get embedding after retries")

def main():
    args = parse_args()
    try:
        api_key = get_api_key_from_anywhere(args.key)
    except RuntimeError as e:
        print(e)
        sys.exit(1)

    print("Using embedding model:", EMBEDDING_MODEL)
    print("Embedding sample texts...")
    sample_embeddings = []
    for i, s in enumerate(samples, 1):
        emb = get_embedding(s, api_key)
        sample_embeddings.append(emb)
        print(f"  embedded {i}/10")
    sample_embeddings = np.vstack(sample_embeddings)
    sample_embeddings = sample_embeddings / (np.linalg.norm(sample_embeddings, axis=1, keepdims=True) + 1e-12)

    query = args.query
    print("\nEmbedding query:", query)
    query_emb = get_embedding(query, api_key)
    query_emb = query_emb / (np.linalg.norm(query_emb) + 1e-12)

    # cosine similarity
    cosine_dists = cdist(query_emb.reshape(1, -1), sample_embeddings, metric="cosine")[0]
    cosine_sims = 1 - cosine_dists

    top_k = 3
    top_k_idx = np.argsort(-cosine_sims)[:top_k]
    print("\nTop-3 similar texts:")
    for rank, idx in enumerate(top_k_idx, start=1):
        print(f"{rank}. (score={cosine_sims[idx]:.4f}) => {samples[idx]}")

    print("\nFull sorted list (score, text):")
    sorted_idx = np.argsort(-cosine_sims)
    for idx in sorted_idx:
        print(f"{cosine_sims[idx]:.4f}  {samples[idx]}")

if __name__ == "__main__":
    main()
