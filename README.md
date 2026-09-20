# Machine Data Management & Local Risk Prediction System

A complete web application for managing machine information and predicting machine risk levels using local machine learning.

## 📋 Overview

This application allows users to:
- **Configure machine fields dynamically** (Text, Number, Dropdown types)
- **Create, view, edit, and delete machine records**
- **Store data persistently** in SQLite database
- **Run local ML predictions** for risk assessment (Low, Medium, High)
- **View results through an intuitive web UI**

## 🏗️ Architecture

```
Web UI (React)
   ↓
FastAPI Backend (Python)
   ↓
SQLite Database ← Machine Records & Field Config
   ↓
Python ML Model (scikit-learn)
   ↓
Risk Prediction (Low/Medium/High)
```

## 🛠️ Technologies Used

| Component | Technology |
|-----------|-----------|
| **Frontend** | React 18 (Embedded in HTML) |
| **Backend** | FastAPI (Python) |
| **Server** | Uvicorn (ASGI server) |
| **Database** | SQLite 3 |
| **Machine Learning** | scikit-learn (Random Forest) |
| **Communication** | REST API (JSON) |

## 📦 Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Initialize Machine Learning Model

```bash
python ml_model.py
```

This creates and saves the trained ML model (`risk_model.pkl`).

### Step 3: Start the Backend Server

```bash
python main.py
```

Expected output:
```
✓ Database initialized
✓ API running on http://127.0.0.1:8000
✓ API docs available at http://127.0.0.1:8000/docs
```

### Step 4: Open the Frontend

In another terminal, start a web server:
```bash
python -m http.server 3000
```

Open your browser and go to: `http://localhost:3000/frontend.html`

**Note**: FastAPI backend runs on port 8000, frontend server on port 3000

## 🎯 How to Use the Application

### 1. Field Configuration Tab
- **View Default Fields**: Machine Name, Temperature, Pressure, Vibration
- **Add New Field**: Click "Add New Field" and configure:
  - Field Name (e.g., "Humidity")
  - Field Type (Text, Number, or Dropdown)
  - Required/Optional status
  - Dropdown options (if applicable)
- **Delete Field**: Click "Delete" next to any field

### 2. Machine Records Tab
- **Create Record**: Click "+ New Machine" and fill the form with configured fields
- **Edit Record**: Click "Edit" on any existing machine
- **Delete Record**: Click "Delete" to remove a machine
- **Auto-generated Form**: The form dynamically generates based on configured fields

### 3. Risk Prediction Tab
- **Select a Machine**: Choose any existing machine from dropdown
- **View Details**: See all machine parameters
- **Run Prediction**: Click "🔍 Run Prediction" to get risk assessment
- **View Result**: Get instant risk level (Low/Medium/High)

## 📊 Machine Learning Model

### Model Type
**Random Forest Classifier** with 10 decision trees

### Features Used
1. **Temperature** (Number): Range 0-100+
2. **Pressure** (Number): Range 0-150+
3. **Vibration** (Dropdown): Low (0), Medium (1), High (2)

### Predictions
- **Low Risk**: Suitable operating conditions
- **Medium Risk**: Monitor required
- **High Risk**: Immediate attention needed

### Example Predictions
```
Input:  Temperature=85, Pressure=120, Vibration=High
Output: High Risk ⚠️

Input:  Temperature=35, Pressure=85, Vibration=Low
Output: Low Risk ✓

Input:  Temperature=55, Pressure=105, Vibration=Medium
Output: Medium Risk ⚠
```

## 🔄 Dynamic Fields & ML Handling

### Scenario: Adding "Humidity" Field

#### 1. How the Application Handles It
- User adds "Humidity" field in Field Configuration tab
- New field immediately available in machine record forms
- Database stores field definition (no schema migration needed)
- Existing records can be updated with humidity values

#### 2. Can Existing ML Model Use It?
**No**, the current model doesn't use Humidity because:
- Model was trained only on: Temperature, Pressure, Vibration
- Adding new input features requires retraining
- Current predictions use only the original 3 features

#### 3. To Use Humidity in ML Predictions

**Option A: Retraining Required** (Recommended)
```python
# 1. Collect training data with humidity values
# 2. Modify ml_model.py to include humidity in features
# 3. Create new training dataset with humidity
# 4. Retrain the model: python ml_model.py
# 5. Restart the application
```

**Option B: Simple Implementation**
Modify `ml_model.py` to add humidity features:

```python
def predict_risk(features):
    # Add humidity to feature extraction
    temperature = float(features.get('Temperature', 50))
    pressure = float(features.get('Pressure', 100))
    vibration = convert_vibration_to_number(features.get('Vibration', 'Low'))
    humidity = float(features.get('Humidity', 50))  # NEW
    
    # Create feature array with 4 features
    X = np.array([[temperature, pressure, vibration, humidity]])
    # ... rest of code
```

**Option C: Ignore New Field**
- New fields in database are ignored by predictions
- Only Temperature, Pressure, Vibration are used
- Application works normally without retraining

### Key Architecture Benefits
- ✅ Database schema doesn't change when adding fields
- ✅ Existing records remain unaffected
- ✅ Field management is independent of ML model
- ✅ Easy to update ML model when needed

## 📁 File Structure

```
.
├── main.py                 # FastAPI backend
├── ml_model.py             # Python ML model (scikit-learn)
├── frontend.html           # React web UI
├── requirements.txt        # Python dependencies
├── machines.db             # SQLite database (auto-created)
├── risk_model.pkl          # Trained ML model (auto-created)
├── .gitignore              # Files to exclude from Git
└── README.md               # This file
```

## 🔌 API Endpoints (FastAPI)

### Field Configuration
```
GET    /api/fields              # Get all fields
POST   /api/fields              # Add new field
DELETE /api/fields/{id}         # Delete field
```

### Machine Records
```
GET    /api/machines            # Get all machines
POST   /api/machines            # Create new machine
GET    /api/machines/{id}       # Get specific machine
PUT    /api/machines/{id}       # Update machine
DELETE /api/machines/{id}       # Delete machine
```

### ML Prediction
```
POST   /api/predict             # Run prediction on machine data
```

### Interactive API Documentation
FastAPI provides automatic API documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

## 🚀 Sample Workflow

1. **Application starts**
   - Backend: `python main.py` (running on port 8000)
   - Database initialized with default fields
   - ML model loaded

2. **User opens frontend.html**
   - React UI loads
   - Fetches field configuration
   - Displays default fields: Machine Name, Temperature, Pressure, Vibration

3. **User adds new field "Humidity"**
   - Field Configuration → Add New Field
   - Type: Number, Required: Yes
   - Field saved to database

4. **User creates a machine record**
   - Machine Records → New Machine
   - Form includes: Machine Name, Temperature, Pressure, Vibration, Humidity
   - Data saved to database

5. **User predicts risk**
   - Risk Prediction → Select Machine
   - Clicks "Run Prediction"
   - Backend sends data to ML model
   - Model uses Temperature, Pressure, Vibration only
   - Returns risk level
   - UI displays result

## 💻 Development Notes

### Extending the ML Model
To improve predictions or add features:

1. Modify training data in `ml_model.py`
2. Update feature extraction in `predict_risk()` function
3. Run: `python ml_model.py` to retrain
4. Restart FastAPI server

### Adding More Field Types
To add new field types (Date, Boolean, etc.):

1. Update field configuration form in `frontend.html`
2. Add database support in `main.py`
3. Add input type in machine records form

### Database Queries
View/debug database:
```bash
sqlite3 machines.db
sqlite> SELECT * FROM field_config;
sqlite> SELECT * FROM machine_records;
```

## ✅ Testing Checklist

- [ ] Application starts without errors
- [ ] Default fields are present
- [ ] Can add new field successfully
- [ ] Can create machine record with all fields
- [ ] Can edit machine record
- [ ] Can delete machine record
- [ ] Can select machine and run prediction
- [ ] Prediction returns Low/Medium/High risk
- [ ] Frontend displays results correctly

## 🆘 Troubleshooting

### Port 8000 Already in Use
```bash
# Kill process on port 8000
# Mac/Linux:
lsof -ti:8000 | xargs kill -9

# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Or change port in main.py (last line):
# uvicorn.run(app, host="127.0.0.1", port=8001)
```

### CORS Errors
- Backend CORS is enabled (FastAPI CORSMiddleware)
- If still getting errors, check frontend URL matches backend

### ML Model Not Working
```bash
# Recreate model
python ml_model.py

# Check if risk_model.pkl exists
ls -la risk_model.pkl
```

### Database Issues
```bash
# Remove old database to reset
rm machines.db

# Application will recreate on startup
python main.py
```

## 📝 Submission Checklist

- [ ] All source code committed to Git
- [ ] `.gitignore` contains: `*.pkl`, `*.db`, `__pycache__`, `.env`
- [ ] README.md with complete documentation
- [ ] No passwords/API keys in repository
- [ ] Application runs with: `python main.py` then open `frontend.html`
- [ ] GitHub repository link shared with assessment team

## 📚 Learning Resources

### Understanding the Code Flow

**Frontend → Backend → Database:**
```
User clicks "Create Machine"
    ↓
React collects form data
    ↓
POST /api/machines with JSON data
    ↓ FastAPI receives and validates data
    ↓
INSERT into machine_records table
    ↓
Response sent back to UI
    ↓
Machine appears in list
```

**Prediction Flow:**
```
User selects machine and clicks "Run Prediction"
    ↓
Frontend sends machine data to /api/predict
    ↓ FastAPI extracts Temperature, Pressure, Vibration
    ↓
Calls ml_model.predict_risk()
    ↓
Model predicts: 0, 1, or 2
    ↓
Converts to: "Low Risk", "Medium Risk", or "High Risk"
    ↓
Returns to frontend with prediction result
    ↓
UI displays risk level with color coding
```

## 🎓 Key Concepts

1. **Dynamic Fields**: Database stores field definitions; no schema change needed
2. **CRUD Operations**: Create, Read, Update, Delete machine records
3. **RESTful API**: Communication using standard HTTP methods
4. **ML Integration**: Local Python model for predictions
5. **Separation of Concerns**: Frontend (UI), Backend (Logic), Database (Storage), ML (Prediction)

## 📞 Support

For issues or questions:
1. Check Troubleshooting section
2. Review API endpoints
3. Check browser console for errors
4. Check FastAPI server logs

---

**Version**: 1.0  
**Last Updated**: 2024  
**Status**: Production Ready ✅
