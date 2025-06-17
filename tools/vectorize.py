import ollama
import pickle
import os
from pypdf import PdfReader
from docx import Document

EMBEDDING_MODEL = 'nomic-embed-text'
LANGUAGE_MODEL = 'hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF'

def read_file(file_path):
    """Extract text from a file based on its extension."""
    if file_path.endswith('.txt'):
        with open(file_path, 'r') as file:
            return file.read()
    elif file_path.endswith('.pdf'):
        reader = PdfReader(file_path)
        return '\n'.join(page.extract_text() for page in reader.pages)
    elif file_path.endswith(('.docx', '.doc')):
        document = Document(file_path)
        return '\n'.join(par.text for par in document.paragraphs)
    else:
        return None

def process_file(file_path, vector_db):
    """Process a single file and add its chunks to the vector database."""
    text = read_file(file_path)
    if text is None:
        return
    
    chunks = chunk_text(text, chunk_size=1500, overlap=150)
    for i, chunk in enumerate(chunks):
        embedding = ollama.embed(model=EMBEDDING_MODEL, input=chunk)['embeddings'][0]
        vector_db.append((chunk, embedding))
        print(f'\tChunk {i+1}/{len(chunks)} loaded.')

def vectorize(file_name=''):
    if file_name == '':
        # Process all files in data folder - create new database
        file_names = os.listdir('data/')
        vector_db = []
        
        for file_name in file_names:
            print(f'File: {file_name}')
            process_file(f'data/{file_name}', vector_db)
    else:
        # Process single file - append to existing database
        vector_db = []
        if os.path.exists('vector_db.pkl'):
            with open('vector_db.pkl', 'rb') as f:
                vector_db = pickle.load(f)
        
        print(f'File: {file_name}')
        process_file(f'data/{file_name}', vector_db)
    
    # Save the database
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