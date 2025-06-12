import ollama
import pickle
import os

EMBEDDING_MODEL = 'nomic-embed-text'
LANGUAGE_MODEL = 'hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF'

def vectorize():
    file_names = os.listdir('data/')
    vector_db = []
    
    for file_name in file_names:
        with open(f'data/{file_name}', 'r') as file:
            print(f'File: {file_name}')
            text = file.read()
            chunks = chunk_text(text, chunk_size=1500, overlap=150)
            for i, chunk in enumerate(chunks):
                embedding = ollama.embed(model=EMBEDDING_MODEL, input=chunk)['embeddings'][0]
                vector_db.append((chunk, embedding))
                print(f'\tChunk {i+1}/{len(chunks)} loaded.')
                
    with open('vector_db.pkl', 'wb') as f:
        pickle.dump(vector_db, f)
        
def chunk_text(text, chunk_size=1500, overlap=150):
    """
    Split text into overlapping chunks of specified size.
    
    Args:
        text (str): The text to chunk
        chunk_size (int): Maximum size of each chunk in characters
        overlap (int): Number of characters to overlap between chunks
    
    Returns:
        list: List of text chunks
    """
    chunks = []
    start = 0
    
    while start < len(text):
        # Calculate end position for this chunk
        end = start + chunk_size
        
        # If this would be the last chunk and it's very small, extend the previous chunk instead
        if end >= len(text):
            chunks.append(text[start:])
            break
        
        # Create the chunk
        chunk = text[start:end]
        chunks.append(chunk)
        
        # Move start position forward by (chunk_size - overlap)
        start += chunk_size - overlap
    
    return chunks