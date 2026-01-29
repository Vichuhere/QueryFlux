# 🚀 QueryFlux - Intelligent PDF Question Answering System

QueryFlux is a **Retrieval-Augmented Generation (RAG)** powered PDF-based question answering and summarization system. Upload one or multiple PDF documents and get instant, accurate answers powered by semantic embeddings and intelligent retrieval strategies.

## 📋 Project Overview

QueryFlux demonstrates practical application of NLP, semantic search, and RAG pipelines in building real-world document intelligence systems. It combines:

- **Text Extraction**: Robust PDF parsing with PyMuPDF (fitz)
- **Smart Chunking**: Semantic paragraph-level document segmentation
- **Embeddings**: Transformer-based semantic representations (Sentence Transformers)
- **Multi-Stage Retrieval**: Direct matching → Semantic search → Fuzzy matching fallback
- **Summarization**: Extractive TF-IDF based document summarization
- **Modern UI**: Interactive Flask-based web interface with drag-and-drop

## 🛠 Tech Stack

| Component | Technology |
|-----------|------------|
| **Web Framework** | Flask 2.3.2 |
| **PDF Processing** | PyMuPDF (fitz) 1.23.8 |
| **Embeddings** | Sentence Transformers 5.2.2 |
| **Similarity Search** | scikit-learn (cosine similarity) |
| **Fuzzy Matching** | fuzzywuzzy 0.18.0 |
| **Summarization** | TF-IDF vectorization |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Python Version** | 3.11+ |

## 📁 Project Structure

```
QueryFlux/
├── app.py                 # Flask application & API routes
├── backend.py             # QueryFluxEngine - Core RAG logic
├── summarizer.py          # Extractive text summarization
├── nltk_setup.py          # Optional NLTK data download
├── req.txt                # Python dependencies
├── templates/
│   └── index.html         # Web UI
├── static/
│   └── style.css          # Professional dark theme CSS
├── data/
│   └── knowledge_base/    # PDF storage directory
└── pdfs/                  # Additional PDF folder (if needed)
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Windows/Linux/Mac

### Installation

1. **Clone/Navigate to project**
```bash
cd D:\E_backup\Queryflux
```

2. **Create Virtual Environment** (if not already created)
```bash
python -m venv .venv
.\.venv\Scripts\activate  # Windows
source .venv/bin/activate # Linux/Mac
```

3. **Install Dependencies**
```bash
pip install -r req.txt
```

This installs:
- Flask (web framework)
- PyMuPDF (PDF text extraction)
- sentence-transformers (semantic embeddings)
- scikit-learn (similarity search)
- fuzzywuzzy (fuzzy string matching)
- And all dependencies

### Running the Application

```bash
# Windows
D:/E_backup/Queryflux/.venv/Scripts/python app.py

# Linux/Mac
python app.py
```

The application will start at: **http://localhost:5000**

## 📖 Usage Guide

### 1. **Upload PDFs**
- Click the upload area or drag-and-drop PDF files
- Click "Upload & Process PDFs"
- System will extract text, create chunks, and generate embeddings
- Wait for success message showing chunk count

### 2. **Ask Questions**
- Enter your question in the input field
- Questions can be:
  - Direct queries: "What is the abstract?"
  - Topic-based: "Explain the methodology"
  - Partial phrases: Works with fuzzy matching
- Click "Get Answer" or press Enter

### 3. **Get Summary** (Optional)
- Check "Include Summary" before asking
- Returns document summary with the answer

### 4. **Clear & Upload New**
- Click "Clear & Upload New" to reset and load different PDFs

## 🧠 How It Works

### RAG Pipeline

#### Stage 1: PDF Processing
```
PDF → Text Extraction → Smart Chunking → Semantic Embeddings
```

- **Text Extraction**: PyMuPDF reads text from all pages
- **Chunking**: Splits text into meaningful paragraphs (>50 chars)
- **Embeddings**: Sentence Transformers (`all-mpnet-base-v2`) generates 768-dim vectors

#### Stage 2: Question Answering (Multi-Stage Retrieval)
```
Question → Embedding → Retrieval → Ranking → Response
```

**Stage 1 - Direct Text Match** (Highest Confidence)
- Searches for exact keyword matches in chunks
- Returns relevant chunks containing query text

**Stage 2 - Semantic Similarity** (If no direct match)
- Encodes question into embedding space
- Uses cosine similarity to find semantically similar chunks
- Returns top-3 matches above 0.35 similarity threshold

**Stage 3 - Fuzzy Matching** (Fallback for typos/variations)
- Levenshtein distance based fuzzy string matching
- Returns best match if score > 50

### Answer Enrichment
- Keywords in the query are **highlighted** in results
- Multiple relevant chunks are separated by "---"
- Maintains original document structure

### Summarization
- TF-IDF vectorization of sentences
- Selects top-5 most important sentences
- Maintains original sentence order

## 🔧 Configuration

### Model Selection
Edit `backend.py` line 17 to use different embeddings:
```python
# Available options:
# self.model = SentenceTransformer("all-mpnet-base-v2")  # Default (Fast)
# self.model = SentenceTransformer("all-MiniLM-L6-v2")   # Lightweight
# self.model = SentenceTransformer("all-distilroberta-v1") # Fast & accurate
```

### Retrieval Parameters
Edit `backend.py` `ask_question()` method:
```python
def ask_question(self, query, top_k=3, threshold=0.35):
    # top_k: Number of results to return (default: 3)
    # threshold: Minimum similarity score (default: 0.35)
```

### Chunk Size
Edit `backend.py` line 24:
```python
self.chunks.clear()
# Minimum chunk size in characters (default: 50)
if len(para) > 50:
    self.chunks.append(para)
```

## 🎨 UI Features

- **Dark Modern Theme**: Professional dark mode interface
- **Drag & Drop**: Upload PDFs by dragging
- **Real-time Status**: Processing indicators and chunk counts
- **Answer Highlighting**: Keywords highlighted in results
- **Responsive Design**: Works on desktop and mobile
- **Copy to Clipboard**: Easily copy answers

## 📊 Performance

- **Embedding Generation**: ~100ms per PDF page
- **Query Response**: ~50-200ms (depending on similarity threshold)
- **Supported File Size**: Up to 100MB per upload
- **Maximum Concurrent Chunks**: No practical limit

## 🐛 Troubleshooting

### "No module named 'X'" Error
```bash
# Reinstall dependencies
pip install -r req.txt
```

### "Please upload and process a PDF first"
- Ensure PDF text is being extracted (not scanned image PDFs)
- Check that PDFs are actual text-based PDFs
- Try with a different PDF

### Slow Embedding Generation
- First run downloads the embedding model (~400MB)
- Subsequent runs use cached model
- Check internet connection if downloading

### PDF Not Being Read
- Ensure PDF is not password protected
- Check if PDF is scanned image (needs OCR - not supported)
- Try with text-based PDFs first

## 📝 Optional: NLTK Setup

For enhanced text processing (optional):
```bash
python nltk_setup.py
```

Downloads additional NLP corpora for better tokenization.

## 🔐 Security Notes

- PDFs are stored in `data/knowledge_base/`
- Server runs on `localhost:5000` by default (not exposed)
- No data is sent to external APIs
- All processing happens locally

## 🚀 Production Deployment

For production use, modify `app.py`:
```python
if __name__ == "__main__":
    # Change debug=True to debug=False
    app.run(debug=False, host="0.0.0.0", port=5000)
    
    # Use production WSGI server:
    # gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 📚 Learning Resources

- [Sentence Transformers Docs](https://www.sbert.net/)
- [PyMuPDF Docs](https://pymupdf.readthedocs.io/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [RAG Concepts](https://www.deeplearning.ai/short-courses/retrieval-augmented-generation-rag/)

## 📄 License

This project is open source and available under MIT License.

## 🤝 Contributing

Improvements welcome! Consider:
- Supporting scanned PDFs with OCR
- Advanced chunking strategies
- Multi-language support
- Custom embedding models
- Database persistence

## 📞 Support

For issues or questions:
1. Check this README
2. Review error messages in terminal
3. Check Flask output logs
4. Verify all dependencies are installed

---

**QueryFlux v1.0** | Powered by RAG, Sentence Transformers & Flask
