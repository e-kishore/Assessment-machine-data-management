# ⚡ Quick Start - 5 Minutes to Working Application

**Don't overthink it! Just follow these steps.**

---

## 📋 Prerequisites
- Python 3.8 or higher installed
- About 2 minutes (first time only)

---

## 🚀 Steps (Choose Your OS)

### For **Linux/Mac** Users:

**Step 1:** Open Terminal and run:
```bash
pip install -r requirements.txt
python ml_model.py
```

**Step 2:** In Terminal 1, run:
```bash
python main.py
```

You'll see:
```
✓ API running on http://127.0.0.1:8000
✓ API docs available at http://127.0.0.1:8000/docs
```

**Step 3:** In Terminal 2, run:
```bash
python -m http.server 3000
```

**Step 4:** Open browser → `http://localhost:3000/frontend.html`

**Done!** ✅

---

### For **Windows** Users:

**Step 1:** Open Command Prompt and run:
```cmd
pip install -r requirements.txt
python ml_model.py
```

Wait for it to complete...

**Step 2:** Open **Command Prompt 1**:
```cmd
python main.py
```

You'll see:
```
✓ API running on http://127.0.0.1:8000
✓ API docs available at http://127.0.0.1:8000/docs
```

**Step 3:** Open **Command Prompt 2**:
```cmd
python -m http.server 3000
```

**Step 4:** Open browser → `http://localhost:3000/frontend.html`

**Done!** ✅

---

### Manual Setup (If Commands Don't Work)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Create ML model
python ml_model.py

# 3. Start FastAPI backend (Terminal 1)
python main.py

# 4. Start web server (Terminal 2)
python -m http.server 3000

# 5. Open browser
# Go to: http://localhost:3000/frontend.html
```

**Note**: FastAPI runs on port 8000, frontend on port 3000

---

## ✅ Testing the Application

### Test 1: Add a Field
1. Click **⚙️ Field Configuration** tab
2. Scroll down to "Current Fields"
3. You should see: Machine Name, Temperature, Pressure, Vibration
4. Scroll up and click **"+ Add Field"**
5. Enter: Field Name = "Humidity", Type = "Number"
6. Check "Required Field"
7. Click **"+ Add Field"** ✅

### Test 2: Create a Machine
1. Click **🤖 Machine Records** tab
2. Click **"+ New Machine"**
3. Fill in:
   - Machine Name: Test Machine
   - Temperature: 75
   - Pressure: 100
   - Vibration: Medium
   - Humidity: 50 (optional, we just added it)
4. Click **"Create"** ✅

### Test 3: Run Prediction
1. Click **📊 Risk Prediction** tab
2. Select machine: "Test Machine"
3. Click **"🔍 Run Prediction"**
4. See result: Low/Medium/High Risk ✅

**If you see results, everything works!**

---

## 🆘 Common Issues & Fixes

### "Port 8000 already in use"
```bash
# Kill the process using port 8000
# Mac/Linux:
lsof -ti:8000 | xargs kill -9

# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### "Port 3000 already in use"
```bash
# Kill the process using port 3000
# Mac/Linux:
lsof -ti:3000 | xargs kill -9

# Windows:
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

### "Module not found" or "pip: command not found"
```bash
# Make sure you have Python 3 installed
python3 --version

# If Python is installed, try:
python3 -m pip install -r requirements.txt
python3 main.py
```

### "Database locked"
Delete `machines.db` and run again:
```bash
rm machines.db
python main.py
```

### Frontend shows blank page
1. Check browser console (F12)
2. Check backend is running on port 8000
3. Clear browser cache (Ctrl+Shift+Del)
4. Try in different browser
5. Check that http://localhost:8000/api/fields works

---

## 📂 What Each File Does

| File | Purpose |
|------|---------|
| `main.py` | FastAPI backend server |
| `ml_model.py` | Machine Learning model (scikit-learn) |
| `frontend.html` | User interface (React) |
| `requirements.txt` | Python dependencies |
| `machines.db` | SQLite database (auto-created) |
| `risk_model.pkl` | ML model file (auto-created) |
| `README.md` | Full documentation |
| `.gitignore` | Files to exclude from Git |

---

## 🎓 What to Do Next

### Option 1: Understand the Code
```bash
# Read README.md - explains everything
# Then read comments in main.py
# Then read comments in ml_model.py
```

### Option 2: Extend the Application
1. Add more fields (Date, Boolean types)
2. Add data visualization (charts)
3. Export records to CSV
4. Add user authentication
5. Deploy to cloud (Heroku, AWS, etc.)

### Option 3: Improve ML Model
1. Add more training data
2. Try different algorithms
3. Tune parameters for better accuracy
4. Add feature importance analysis

---

## 📚 Documentation Files

- **QUICK_START.md** ← You are here (5 min setup)
- **README.md** (complete reference)
- **Code comments** (in each Python file)

---

## ✨ Pro Tips

1. **Keep TWO terminals open** - one for FastAPI, one for web server
   - Terminal 1: `python main.py` (FastAPI on port 8000)
   - Terminal 2: `python -m http.server 3000` (Frontend on port 3000)
2. **Check browser console** (F12) if things don't work
3. **Check FastAPI docs** at http://localhost:8000/docs to test API
4. **Read error messages** - they usually tell you what's wrong
5. **Refresh browser** when you restart backend
6. **Use Chrome DevTools** to debug frontend issues

---

## 🎯 Success Criteria

- [ ] Application starts without errors
- [ ] See 4 default fields
- [ ] Can add new field "Humidity"
- [ ] Can create machine with all fields
- [ ] Can select machine and get prediction result
- [ ] Result shows Low/Medium/High Risk

**All 6 checked? You're done!** 🎉

---

## 📞 Getting Help

**If stuck:**
1. Re-read relevant section above
2. Check error message carefully
3. Try refreshing/restarting
4. Check common issues section
5. Read README.md for concepts

**Most issues are solved by:**
- Restarting both terminals
- Clearing browser cache
- Deleting machines.db and starting fresh
- Checking that both ports 8000 and 3000 are free

---

## ⏱️ Time Estimates

- Setup: 2 minutes
- Testing: 5 minutes
- **Total: ~7 minutes**

You can have a working application **right now**! 🚀

---

**Stop reading, start doing! Run the installation now!** 💪
