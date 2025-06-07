#%%
dataset = []
with open('data/hoa-regulations.txt', 'r') as file:
    dataset = file.read().split('---')
print(len(dataset), "chunks")
# %%
import ollama

EMBEDDING_MODEL = 'nomic-embed-text'
LANGUAGE_MODEL = 'hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF'

VECTOR_DB = []

def add_chunk_to_database(chunk):
    embedding = ollama.embed(model=EMBEDDING_MODEL, input=chunk)['embeddings'][0]
    VECTOR_DB.append((chunk, embedding))
    
for i, chunk in enumerate(dataset):
    add_chunk_to_database(chunk)
    print(f'Added chunk {i+1}/{len(dataset)} to the database')
# %%
import pickle

with open('vector_db.pkl', 'wb') as f:
    pickle.dump(VECTOR_DB, f)
# %%
print(VECTOR_DB)
# %%
