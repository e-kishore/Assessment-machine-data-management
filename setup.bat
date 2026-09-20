@echo off
REM Machine Data Management - Setup Script for Windows

echo.
echo ========================================
echo 🚀 Setting up Application (Windows)
echo ========================================
echo.

REM Check Python
echo ✓ Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo    Download from: https://www.python.org/
    echo    Make sure to check "Add Python to PATH"
    pause
    exit /b 1
)

python --version
echo.

REM Install dependencies
echo 📦 Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)
echo ✓ Dependencies installed
echo.

REM Create ML model
echo 🤖 Training ML model...
python ml_model.py
if errorlevel 1 (
    echo ❌ Failed to create ML model
    pause
    exit /b 1
)
echo ✓ ML model created (risk_model.pkl)
echo.

echo.
echo ========================================
echo ✅ Setup complete!
echo ========================================
echo.
echo 🎯 Next steps:
echo.
echo 1️⃣  Start the FastAPI backend server (CMD 1):
echo    python main.py
echo.
echo 2️⃣  In another Command Prompt (CMD 2), start web server:
echo    python -m http.server 3000
echo.
echo 3️⃣  Open browser and go to:
echo    http://localhost:3000/frontend.html
echo.
echo 💡 FastAPI runs on: http://localhost:8000
echo 📚 API docs at: http://localhost:8000/docs
echo.
echo ========================================
echo 📚 Read LEARNING_GUIDE.md to understand everything
echo 📖 Read README.md for full documentation
echo ========================================
echo.
pause