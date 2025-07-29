# backend.py

import os
import re
import fitz  # PyMuPDF
from fuzzywuzzy import fuzz
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer


class QueryFluxEngine:
    def __init__(self, pdf_folder: str, chunk_size=500, overlap=100):
        self.pdf_folder = pdf_folder
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.chunks = []
        self.embeddings = None
        self.model = SentenceTransformer("all-mpnet-base-v2")

    def load_and_chunk_pdfs(self):
        self.chunks.clear()

        for filename in os.listdir(self.pdf_folder):
            if filename.endswith(".pdf"):
                file_path = os.path.join(self.pdf_folder, filename)
                doc = fitz.open(file_path)
                text = ""

                for page in doc:
                    text += page.get_text()

                doc.close()

                # Smart paragraph/sentence splitting
                paragraphs = re.split(r"\n\s*\n|(?<=[.!?])\s+", text)
                for para in paragraphs:
                    para = para.strip()
                    if len(para) > 50:
                        self.chunks.append(para)

        return len(self.chunks)

    def embed_chunks(self):
        if not self.chunks:
            raise ValueError("Chunks are empty. Load and chunk PDFs first.")

        self.embeddings = self.model.encode(self.chunks)

    @staticmethod
    def highlight_keywords(text, keywords):
        for keyword in keywords:
            pattern = re.compile(re.escape(keyword), re.IGNORECASE)
            text = pattern.sub(lambda m: f"<mark>{m.group(0)}</mark>", text)
        return text

    def ask_question(self, query, top_k=3, threshold=0.4):
        if self.embeddings is None or not self.chunks:
            raise ValueError("🚫 Please upload and process a PDF first.")

        query_lower = query.lower()

        # 🔍 Direct match (entire paragraph containing query text)
        direct_matches = []
        for chunk in self.chunks:
            if query_lower in chunk.lower():
                direct_matches.append(chunk)
                if len(direct_matches) == top_k:
                    break

        if direct_matches:
            highlighted = [self.highlight_keywords(chunk, query_lower.split()) for chunk in direct_matches]
            return "\n\n---\n\n".join(highlighted)

        # 🤖 Embedding-based semantic search
        query_embedding = self.model.encode([query_lower])
        similarities = cosine_similarity(query_embedding, self.embeddings)[0]
        top_indices = similarities.argsort()[::-1]

        results = []
        for idx in top_indices:
            if similarities[idx] >= threshold:
                results.append(self.chunks[idx])
            if len(results) == top_k:
                break

        if results:
            highlighted = [self.highlight_keywords(chunk, query_lower.split()) for chunk in results]
            return "\n\n---\n\n".join(highlighted)

        # 🧠 Fuzzy fallback
        best_match = ""
        best_score = 0
        for chunk in self.chunks:
            score = fuzz.partial_ratio(query_lower, chunk)
            if score > best_score:
                best_score = score
                best_match = chunk

        if best_score > 60:
            return f"(Fuzzy Matched 🔍)\n\n{best_match}"

        return "🤷 No relevant answer found even with fuzzy or embedding search."
