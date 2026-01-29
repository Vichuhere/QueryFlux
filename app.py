# app.py
"""
QueryFlux - Flask Web Application
RAG-based PDF Question Answering and Summarization System
"""

from flask import Flask, render_template, request, jsonify
import os
from backend import QueryFluxEngine
from summarizer import summarize_text

UPLOAD_FOLDER = "data/knowledge_base"
ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 100 * 1024 * 1024  # 100MB max file size

# Global engine instance
engine = None


def allowed_file(filename):
    """Check if file has allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def init_engine():
    """Initialize or reinitialize the QueryFlux engine"""
    global engine
    # Ensure upload folder exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    engine = QueryFluxEngine(pdf_folder=UPLOAD_FOLDER)
    return engine


@app.route("/")
def index():
    """Serve the main HTML page"""
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    """
    Handle PDF file uploads
    Process uploaded PDFs: extract text, create chunks, generate embeddings
    """
    global engine
    
    print("\n" + "="*60)
    print("📤 UPLOAD REQUEST RECEIVED")
    print("="*60)
    
    # Check if files were provided
    uploaded_files = request.files.getlist("pdfs")
    if not uploaded_files or all(f.filename == '' for f in uploaded_files):
        return jsonify({
            "success": False,
            "message": "⚠️ No PDF files selected"
        }), 400

    # Filter for valid PDF files
    valid_files = [f for f in uploaded_files if f and allowed_file(f.filename)]
    if not valid_files:
        return jsonify({
            "success": False,
            "message": "⚠️ Only PDF files are allowed"
        }), 400

    try:
        # Create upload folder
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        # Save uploaded files
        saved_files = []
        for uploaded_file in valid_files:
            filename = uploaded_file.filename
            save_path = os.path.join(UPLOAD_FOLDER, filename)
            uploaded_file.save(save_path)
            saved_files.append(filename)
            print(f"✓ Saved: {filename}")

        # Reinitialize engine for fresh processing
        print(f"\n🔄 Initializing QueryFlux Engine...")
        engine = init_engine()

        # Load and process PDFs
        print(f"\n📖 Processing {len(saved_files)} PDF(s)...")
        chunks_count = engine.load_and_chunk_pdfs()

        if chunks_count == 0:
            return jsonify({
                "success": False,
                "message": "❌ No valid text chunks created. Check that:\n1. PDFs contain actual text (not scanned images)\n2. PDFs are not password protected\n3. Try uploading a different PDF file"
            }), 400

        # Generate embeddings
        print(f"\n🧠 Generating semantic embeddings...")
        engine.embed_chunks()

        message = f"✅ Successfully processed {len(saved_files)} PDF(s)!\n📊 Created {chunks_count} text chunks and generated embeddings.\n\n💬 You can now ask questions about the document!"
        
        print(f"\n{message}")
        print("="*60 + "\n")
        
        return jsonify({
            "success": True,
            "message": message,
            "chunks": chunks_count,
            "files": saved_files
        })

    except Exception as e:
        error_msg = f"❌ Error processing PDFs: {str(e)}"
        print(f"\n{error_msg}")
        print("="*60 + "\n")
        return jsonify({
            "success": False,
            "message": error_msg
        }), 500


@app.route("/ask", methods=["POST"])
def ask():
    """
    Handle question answering requests
    Uses the processed PDFs and RAG to retrieve relevant answers
    """
    global engine
    
    data = request.get_json()
    question = data.get("question", "").strip()
    
    print("\n" + "="*60)
    print(f"❓ QUESTION: {question}")
    print("="*60)

    if not question:
        return jsonify({
            "success": False,
            "message": "⚠️ Please enter a question"
        }), 400

    # Check if engine is initialized with PDFs
    if engine is None or not engine.chunks or engine.embeddings is None:
        return jsonify({
            "success": False,
            "message": "❌ Please upload and process a PDF first"
        }), 400

    try:
        # Get answer using RAG
        answer = engine.ask_question(question)
        
        # Optional: Generate summary if requested
        summary = None
        if data.get("include_summary"):
            print(f"\n📄 Generating summary...")
            summary_text = " ".join(engine.chunks)
            summary = summarize_text(summary_text, num_sentences=5)
            print(f"✓ Summary generated")

        print(f"\n✓ Answer retrieved successfully")
        print("="*60 + "\n")

        return jsonify({
            "success": True,
            "answer": answer,
            "summary": summary
        })

    except Exception as e:
        error_msg = f"❌ Error retrieving answer: {str(e)}"
        print(f"\n{error_msg}")
        print("="*60 + "\n")
        return jsonify({
            "success": False,
            "message": error_msg
        }), 500


@app.route("/status", methods=["GET"])
def status():
    """Get the current status of the engine"""
    global engine
    
    if engine is None or not engine.chunks:
        return jsonify({
            "ready": False,
            "chunks": 0,
            "message": "No PDFs loaded"
        })
    
    return jsonify({
        "ready": True,
        "chunks": len(engine.chunks),
        "has_embeddings": engine.embeddings is not None,
        "message": f"Ready with {len(engine.chunks)} chunks"
    })


@app.route("/clear", methods=["POST"])
def clear():
    """Clear all loaded PDFs and reset the engine"""
    global engine
    
    try:
        # Delete files from upload folder
        if os.path.exists(UPLOAD_FOLDER):
            for filename in os.listdir(UPLOAD_FOLDER):
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
        
        # Reset engine
        engine = None
        
        return jsonify({
            "success": True,
            "message": "✓ All PDFs cleared. Ready for new uploads."
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error clearing PDFs: {str(e)}"
        }), 500


# Initialize engine on startup
init_engine()

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🚀 QueryFlux - PDF Q&A System")
    print("="*60)
    print("📝 Starting Flask server...")
    print("🌐 Open http://localhost:5000 in your browser")
    print("="*60 + "\n")
    
    app.run(debug=True, host="0.0.0.0", port=5000)

