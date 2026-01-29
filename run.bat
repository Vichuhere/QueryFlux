@echo off
REM QueryFlux - Startup Script for Windows
REM This script starts the Flask application

echo.
echo ====================================================================
echo  🚀 QueryFlux - PDF Question Answering & Summarization System
echo ====================================================================
echo.

REM Check if virtual environment exists
if not exist ".venv\" (
    echo ❌ Virtual environment not found!
    echo Creating virtual environment...
    python -m venv .venv
    echo ✓ Virtual environment created
    echo.
    echo Installing dependencies...
    .\.venv\Scripts\pip install -r req.txt
    echo ✓ Dependencies installed
    echo.
)

REM Activate virtual environment and start Flask
echo Starting QueryFlux...
echo.
.\.venv\Scripts\python app.py

REM If Flask stops, show message
echo.
echo ====================================================================
echo  Flask application stopped
echo ====================================================================
pause
