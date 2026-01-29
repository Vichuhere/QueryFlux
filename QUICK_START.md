# QueryFlux - Quick Commands Reference

## 🚀 Start Application

### Windows
```bash
# Option 1: Double-click
run.bat

# Option 2: Terminal
D:/E_backup/Queryflux/.venv/Scripts/python app.py
```

### Linux/Mac
```bash
# Option 1: Shell script
./run.sh

# Option 2: Terminal
python app.py
```

---

## 🔧 Setup & Installation

### First Time Setup (if needed)
```bash
# Create virtual environment
python -m venv .venv

# Activate environment
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Install dependencies
pip install -r req.txt
```

### Update Dependencies
```bash
pip install -r req.txt --upgrade
```

### Check Installed Packages
```bash
pip list
```

---

## 🧠 Optional: Download NLTK Data
```bash
python nltk_setup.py
```

---

## 📂 File Locations

- **Web UI**: `templates/index.html`
- **Styling**: `static/style.css`
- **Backend Logic**: `backend.py`
- **Flask App**: `app.py`
- **PDFs Storage**: `data/knowledge_base/`
- **Config**: `req.txt`

---

## 🌐 Access Application

Once Flask is running, open browser:
```
http://localhost:5000
```

---

## 🔍 Debugging

### Check Flask Output
Flask will print:
- PDF processing status
- Chunks created
- Embeddings generated
- Query search stages

### Check Browser Console
Press `F12` → Console tab to see JavaScript errors

### Verify Setup
```bash
python -c "from app import app; print('✓ App imports OK')"
```

---

## 📊 Project Structure Quick Reference

```
d:\E_backup\Queryflux\
├── app.py                    # Flask application
├── backend.py                # RAG engine
├── summarizer.py             # Summarization
├── nltk_setup.py             # NLTK setup
├── req.txt                   # Dependencies
├── README.md                 # User guide
├── PROJECT_SUMMARY.md        # This project overview
├── run.bat                   # Windows startup
├── run.sh                    # Linux/Mac startup
├── templates/
│   └── index.html           # Web interface
├── static/
│   └── style.css            # Styling
└── data/
    └── knowledge_base/      # PDF storage
```

---

## ✅ Verification Steps

### 1. Check Python Version
```bash
python --version
# Should be 3.11+
```

### 2. Verify Virtual Environment
```bash
which python
# Should show path to .venv
```

### 3. Test Imports
```bash
python -c "from flask import Flask; from sentence_transformers import SentenceTransformer; print('✓ All imports OK')"
```

### 4. Test Flask App
```bash
python -c "from app import app; print('✓ Flask app loads correctly')"
```

---

## 🐛 Troubleshooting Quick Fixes

### "Module not found" error
```bash
pip install -r req.txt
```

### Port 5000 already in use
Kill the process or use different port:
```bash
# In app.py, change: app.run(port=5001)
```

### PDF not being read
- Ensure PDF is text-based (not scanned image)
- Try with a different PDF file
- Check file is not corrupted

### Slow on first run
- First run downloads 400MB+ embedding model
- Subsequent runs are fast
- Check internet connection

---

## 📈 Performance Tips

1. **Faster Startup**: Use lighter embedding model
   - Edit `backend.py` line 17
   - Try `all-MiniLM-L6-v2` instead

2. **Faster Queries**: Lower similarity threshold
   - Edit `ask_question(threshold=0.25)`

3. **More Accurate**: Increase similarity threshold
   - Edit `ask_question(threshold=0.50)`

---

## 🔒 Security Notes

- PDFs stored locally in `data/knowledge_base/`
- No data sent to cloud services
- All processing happens on your machine
- Server runs on localhost (not exposed)

---

## 📞 Support Resources

### Within Project
1. **README.md** - Complete documentation
2. **PROJECT_SUMMARY.md** - Architecture overview
3. **app.py** - Flask routes and comments
4. **backend.py** - QueryFlux engine with docstrings

### External Resources
- Sentence Transformers: https://www.sbert.net/
- Flask: https://flask.palletsprojects.com/
- PyMuPDF: https://pymupdf.readthedocs.io/
- scikit-learn: https://scikit-learn.org/

---

## 🎯 Common Tasks

### Upload and Query PDFs
1. Start: `python app.py`
2. Open: `http://localhost:5000`
3. Upload: Drag PDF or click
4. Wait for success message
5. Ask question
6. View answer with highlights

### Get Document Summary
1. Upload PDFs (as above)
2. Check "Include Summary" checkbox
3. Ask any question
4. View both answer and summary

### Clear and Upload New PDFs
1. Click "Clear & Upload New" button
2. Select new PDF files
3. Upload and process

### Stop Application
- Press `Ctrl+C` in terminal

---

## 💾 Saving Work

### Export Answer
1. Click answer box
2. Click "Copy" button
3. Paste anywhere

### Save PDFs
- Uploaded PDFs automatically saved in `data/knowledge_base/`
- Delete files directly from this folder to clear them

---

**QueryFlux v1.0 - Ready to Use!**

Last Updated: January 29, 2026
