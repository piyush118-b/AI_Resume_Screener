from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# 🌟 1. Loading the Math Brain
# We are downloading a tiny, super-fast AI model from Hugging Face.
# This model takes English text and turns it into a list of 384 numbers (a Vector).
print("Loading Sentence Transformer Model (This might take a second)...")
model = SentenceTransformer('all-MiniLM-L6-v2') 
print("Model Loaded!")

def calculate_match_score(resume_text: str, job_description_text: str) -> float:
    """
    This function takes two pieces of text and calculates how similar they are.
    It solves the "Machine Learning" vs "Artificial Intelligence" problem!
    """
    
    # 🌟 2. Converting Words to Numbers (Embeddings)
    # The computer doesn't understand english. It only understands numbers.
    # We ask our AI model to read the texts and convert their meaning into an array of numbers.
    # Example: "Apple" might become [0.2, 0.5, -0.1...]
    
    # We pass our text into the model to encode it into "Embeddings" (Vectors)
    resume_vector = model.encode([resume_text])
    job_vector = model.encode([job_description_text])
    
    # 🌟 3. The Math Magic (Cosine Similarity)
    # Imagine drawing two lines on a graph originating from zero. 
    # One line represents the resume, one line represents the job.
    # If the lines point in the exact same direction, the person is a 100% match!
    # If they point in opposite directions, it's a 0% match.
    # Cosine Similarity measures the angle between these two lines.
    
    # We calculate the similarity and get a number between 0 and 1
    similarity_matrix = cosine_similarity(resume_vector, job_vector)
    
    # Extract the single number from the matrix
    raw_score = similarity_matrix[0][0]
    
    # Convert it to a percentage (e.g., 0.85 -> 85.0) and round it nicely
    percentage_score = round(raw_score * 100, 2)
    
    # We don't want negative scores, so if it's below zero, we just say 0
    return max(0.0, percentage_score)
