# backend.py
import os
import re
import fitz  # PyMuPDF
from fuzzywuzzy import fuzz
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import numpy as np


class QueryFluxEngine:
    """
    QueryFlux - Retrieval-Augmented Generation (RAG) system for PDF-based Q&A
    
    This engine:
    1. Extracts text from PDF documents
    2. Chunks text into semantic paragraphs
    3. Generates embeddings using sentence transformers
    4. Retrieves relevant chunks using multiple strategies (semantic, fuzzy, direct)
    5. Returns highlighted answers with source context
    """
    
    def __init__(self, pdf_folder: str, chunk_size=500, overlap=100):
        """Initialize the QueryFlux engine with a PDF folder path"""
        self.pdf_folder = pdf_folder
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.chunks = []
        self.embeddings = None
        self.model = SentenceTransformer("all-mpnet-base-v2")
        print(f"✓ QueryFlux Engine initialized | Model: all-mpnet-base-v2")

    def load_and_chunk_pdfs(self):
        """
        Load all PDFs from folder, extract text, and chunk into paragraphs
        Returns: Number of chunks created
        """
        self.chunks.clear()

        # Ensure pdf_folder exists
        if not os.path.exists(self.pdf_folder):
            print(f"✗ PDF folder does not exist: {self.pdf_folder}")
            return 0

        abs_path = os.path.abspath(self.pdf_folder)
        print(f"\n📂 Loading PDFs from: {abs_path}")
        
        files_in_folder = os.listdir(self.pdf_folder)
        pdf_files = [f for f in files_in_folder if f.endswith(".pdf")]
        
        if not pdf_files:
            print(f"✗ No PDF files found in folder")
            return 0
        
        print(f"📄 Found {len(pdf_files)} PDF file(s): {pdf_files}\n")

        for filename in pdf_files:
            file_path = os.path.join(self.pdf_folder, filename)
            print(f"  Processing: {filename}")
            
            try:
                doc = fitz.open(file_path)
                text = ""
                page_count = len(doc)

                for page_num in range(page_count):
                    page = doc[page_num]
                    page_text = page.get_text()
                    text += page_text
                    print(f"    Page {page_num + 1}/{page_count}: {len(page_text)} chars")

                text = text.strip()
                print(f"    Total extracted: {len(text)} characters")
                
                if not text:
                    print(f"    ✗ No text extracted (PDF might be scanned/image-based)")
                    doc.close()
                    continue

                print(f"    ✓ Extracted from {page_count} pages")

                # Smart paragraph/sentence splitting
                # Split by double newlines or sentence endings
                paragraphs = re.split(r"\n\s*\n|(?<=[.!?])\s+", text)
                print(f"    Found {len(paragraphs)} potential chunks (before filtering)")
                
                chunk_count = 0
                short_chunks = []
                
                for para in paragraphs:
                    para = para.strip()
                    # Keep chunks with more than 20 chars (lowered from 50)
                    if len(para) > 20:
                        self.chunks.append(para)
                        chunk_count += 1
                    elif len(para) > 0:
                        short_chunks.append(len(para))
                
                print(f"    ✓ Created {chunk_count} chunks (filtered from {len(paragraphs)})")
                if short_chunks:
                    print(f"    (Filtered out {len(short_chunks)} short chunks)")
                
                doc.close()
                
            except Exception as e:
                print(f"    ✗ Error: {str(e)}")
                try:
                    doc.close()
                except:
                    pass
                continue

        total = len(self.chunks)
        print(f"\n✓ Total chunks created: {total}")
        if total > 0:
            print(f"  Average chunk size: {len(' '.join(self.chunks)) // total} chars")
        return total

    def embed_chunks(self):
        """
        Generate semantic embeddings for all chunks using sentence transformers
        """
        if not self.chunks:
            raise ValueError("No chunks available. Load and chunk PDFs first.")

        print(f"\n🧠 Generating embeddings for {len(self.chunks)} chunks...")
        self.embeddings = self.model.encode(self.chunks, show_progress_bar=False)
        print(f"✓ Embeddings generated | Shape: {self.embeddings.shape}")

    @staticmethod
    def highlight_keywords(text, keywords):
        """Highlight keywords in text with HTML <mark> tags"""
        for keyword in keywords:
            pattern = re.compile(re.escape(keyword), re.IGNORECASE)
            text = pattern.sub(lambda m: f"<mark>{m.group(0)}</mark>", text)
        return text

    def ask_question(self, query, top_k=3, threshold=0.35):
        """
        RAG-based question answering with multi-stage retrieval strategy:
        1. Direct text matching (highest precision)
        2. Semantic similarity search (embedding-based)
        3. Fuzzy matching fallback (handles typos/variations)
        """
        if self.embeddings is None or not self.chunks:
            raise ValueError("Please upload and process a PDF first.")

        query_lower = query.lower()
        
        # Stage 1: Direct text match (highest confidence)
        print(f"\n🔍 Searching for: '{query}'")
        direct_matches = []
        for chunk in self.chunks:
            if query_lower in chunk.lower():
                direct_matches.append(chunk)
                if len(direct_matches) == top_k:
                    break

        if direct_matches:
            print(f"  ✓ Found {len(direct_matches)} direct text matches")
            highlighted = [self.highlight_keywords(chunk, query_lower.split()) for chunk in direct_matches]
            return "\n\n---\n\n".join(highlighted)

        # Stage 2: Semantic similarity search
        print(f"  No direct match, using semantic search...")
        query_embedding = self.model.encode([query_lower])
        similarities = cosine_similarity(query_embedding, self.embeddings)[0]
        top_indices = similarities.argsort()[::-1]

        results = []
        for idx in top_indices:
            if similarities[idx] >= threshold:
                results.append((self.chunks[idx], similarities[idx]))
            if len(results) == top_k:
                break

        if results:
            print(f"  ✓ Found {len(results)} semantic matches")
            chunks_only = [r[0] for r in results]
            highlighted = [self.highlight_keywords(chunk, query_lower.split()) for chunk in chunks_only]
            return "\n\n---\n\n".join(highlighted)

        # Stage 3: Fuzzy matching fallback (tolerates typos)
        print(f"  No semantic match, using fuzzy search...")
        best_match = ""
        best_score = 0
        for chunk in self.chunks:
            score = fuzz.partial_ratio(query_lower, chunk.lower())
            if score > best_score:
                best_score = score
                best_match = chunk

        if best_score > 50:
            print(f"  ✓ Fuzzy match found (score: {best_score})")
            return f"{best_match}"

        print(f"  ✗ No answer found")
        return "No relevant answer found. Try rephrasing your question or upload documents with related content."
