# summarizer.py
"""
Extractive text summarization using TF-IDF and cosine similarity
Extracts the most important sentences from the text
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def summarize_text(text, num_sentences=5):
    """
    Generate an extractive summary of the text using TF-IDF
    
    Args:
        text: Input text to summarize
        num_sentences: Number of sentences to include in summary
    
    Returns:
        Summary text with the most important sentences
    """
    # Split text into sentences
    sentences = text.split('.')
    sentences = [s.strip() for s in sentences if len(s.strip()) > 10]

    # If text is shorter than requested summary, return full text
    if len(sentences) <= num_sentences:
        return '. '.join(sentences)

    try:
        # Vectorize sentences using TF-IDF
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(sentences)
        
        # Calculate cosine similarity
        similarity_matrix = cosine_similarity(tfidf_matrix)
        
        # Calculate importance scores by summing similarities
        importance_scores = similarity_matrix.sum(axis=1)
        
        # Get indices of top sentences
        top_indices = np.argsort(importance_scores)[-num_sentences:]
        top_indices = sorted(top_indices)  # Maintain original order
        
        # Construct summary
        summary_sentences = [sentences[i] for i in top_indices]
        summary = '. '.join(summary_sentences) + '.'
        
        return summary
        
    except Exception as e:
        print(f"Error during summarization: {str(e)}")
        # Fallback: return first num_sentences
        return '. '.join(sentences[:num_sentences]) + '.'
