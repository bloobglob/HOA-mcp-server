#%%
from fastmcp import FastMCP

mcp = FastMCP('HOA-mcp-server')

@mcp.tool
def retrieve_context(prompt: str) -> str:
    print('tool called')
    r_list = retrieve(prompt)
    r_str = ''
    for r in r_list:
        r_str += r[0]
    return r_str
    
#%%
import ollama
import pickle

EMBEDDING_MODEL = 'nomic-embed-text'
LANGUAGE_MODEL = 'hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF'

with open('vector_db.pkl', 'rb') as f:
    VECTOR_DB = pickle.load(f)

def cosine_similarity(a, b):
    dot_product = sum([x * y for x, y in zip(a, b)])
    norm_a = sum([x ** 2 for x in a]) ** 0.5
    norm_b = sum([x ** 2 for x in b]) ** 0.5
    return dot_product / (norm_a * norm_b)

def retrieve(query, top_n=3):
    query_embedding = ollama.embed(model=EMBEDDING_MODEL, input=query)['embeddings'][0]
    # temporary list to store (chunk, similarity) pairs
    similarities = []
    for chunk, embedding in VECTOR_DB:
        similarity = cosine_similarity(query_embedding, embedding)
        similarities.append((chunk, similarity))
    # sort by similarity in descending order, because higher similarity means more relevant chunks
    similarities.sort(key=lambda x: x[1], reverse=True)
    # finally, return the top N most relevant chunks
    return similarities[:top_n]

#%%
def main():
    mcp.run(transport='streamable-http')

if __name__ == "__main__":
    main()