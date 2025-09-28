"""
Simple function to get embeddings for any text using GEMINI API
"""

import os
import numpy as np
from dotenv import load_dotenv
from google import genai
from google.genai import types


def get_embeddings(text):
    """
    Get vector embedding for the given text using GEMINI API.

    Args:
        text (str): The text to generate embeddings for

    Returns:
        numpy.ndarray: The embedding vector
    """
    # Load API key
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key or api_key == "your_gemini_api_key_here":
        raise ValueError("GEMINI_API_KEY not found in .env file")

    # Create client
    client = genai.Client(api_key=api_key)

    # Generate embedding
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text,
        config=types.EmbedContentConfig(task_type="SEMANTIC_SIMILARITY"),
    )

    # Return the embedding vector as numpy array
    return np.array(result.embeddings[0].values)


# Example usage
if __name__ == "__main__":
    # Test the function
    text = "Hello, world!"
    embedding = get_embeddings(text)
    print(f"Text: {text}")
    print(f"Embedding shape: {embedding.shape}")
    print(f"First 5 values: {embedding[:5]}")