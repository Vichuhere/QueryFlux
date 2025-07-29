# summarizer.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def summarize_text(text, num_sentences=5):
    sentences = text.split('.')
    sentences = [s.strip() for s in sentences if len(s.strip()) > 10]

    if len(sentences) <= num_sentences:
        return text

    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform(sentences)
    scores = cosine_similarity(tfidf[0:1], tfidf).flatten()
    ranked_sentences = [s for _, s in sorted(zip(scores, sentences), reverse=True)]
    return ". ".join(ranked_sentences[:num_sentences])
