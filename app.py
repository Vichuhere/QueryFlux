# app.py
from flask import Flask, render_template, request
import os
from backend import QueryFluxEngine
from summarizer import summarize_text

UPLOAD_FOLDER = "data/knowledge_base"

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Initialize engine
engine = QueryFluxEngine(pdf_folder=UPLOAD_FOLDER)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    uploaded_files = request.files.getlist("pdfs")
    if not uploaded_files:
        return render_template("index.html", result="⚠️ No files selected.")

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    for uploaded_file in uploaded_files:
        if uploaded_file.filename.endswith(".pdf"):
            save_path = os.path.join(app.config["UPLOAD_FOLDER"], uploaded_file.filename)
            uploaded_file.save(save_path)

    try:
        chunks_count = engine.load_and_chunk_pdfs()
        engine.embed_chunks()
        return render_template("index.html", result=f"✅ {chunks_count} chunks created and indexed!")
    except Exception as e:
        return render_template("index.html", result=f"❌ Error processing PDFs: {e}")

@app.route("/ask", methods=["POST"])
def ask():
    question = request.form.get("question")
    if not question:
        return render_template("index.html", result="⚠️ Please enter a question.")

    show_summary = "summary" in request.form

    try:
        result = engine.ask_question(question)
        if show_summary:
            summary = summarize_text(" ".join(engine.chunks))
            result += f"\n\n📄 Summary:\n{summary}"
        return render_template("index.html", result=result)
    except Exception as e:
        return render_template("index.html", result=f"❌ Error: {e}")

if __name__ == "__main__":
    app.run(debug=True)
