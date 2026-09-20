"""
Machine Data Management Backend - FastAPI Version
Simple FastAPI application with database and ML integration
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import sqlite3
import json
import os
from ml_model import predict_risk
from datetime import datetime

# Initialize FastAPI app
app = FastAPI(
    title="Machine Data Management API",
    description="API for managing machine data and risk prediction"
)

# Enable CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE = 'machines.db'

# ============ PYDANTIC MODELS ============

class FieldConfig(BaseModel):
    field_name: str
    field_type: str
    is_required: bool = True
    dropdown_options: Optional[List[str]] = None

class FieldResponse(BaseModel):
    id: int
    field_name: str
    field_type: str
    is_required: bool
    dropdown_options: Optional[List[str]] = None

class MachineRecord(BaseModel):
    pass  # Dynamic - accepts any data

class MachineResponse(BaseModel):
    id: int
    data: dict
    created_at: str
    updated_at: str

class PredictionRequest(BaseModel):
    pass  # Dynamic - accepts any data

class PredictionResponse(BaseModel):
    success: bool
    risk_level: str
    features_used: dict

# ============ DATABASE FUNCTIONS ============

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database tables"""
    if os.path.exists(DATABASE):
        return
    
    conn = get_db()
    c = conn.cursor()
    
    # Table for field configuration
    c.execute('''CREATE TABLE field_config
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  field_name TEXT NOT NULL UNIQUE,
                  field_type TEXT NOT NULL,
                  is_required BOOLEAN NOT NULL,
                  dropdown_options TEXT)''')
    
    # Table for machine records
    c.execute('''CREATE TABLE machine_records
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  record_data TEXT NOT NULL,
                  created_at TIMESTAMP,
                  updated_at TIMESTAMP)''')
    
    # Insert default fields
    default_fields = [
        ('Machine Name', 'Text', True, None),
        ('Temperature', 'Number', True, None),
        ('Pressure', 'Number', True, None),
        ('Vibration', 'Dropdown', True, 'Low,Medium,High')
    ]
    
    for field_name, field_type, is_required, dropdown_options in default_fields:
        c.execute('''INSERT INTO field_config (field_name, field_type, is_required, dropdown_options)
                     VALUES (?, ?, ?, ?)''',
                  (field_name, field_type, is_required, dropdown_options))
    
    conn.commit()
    conn.close()

# ============ FIELD CONFIGURATION ENDPOINTS ============

@app.get("/api/fields", response_model=List[FieldResponse])
async def get_fields():
    """Get all configured fields"""
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM field_config')
    fields = c.fetchall()
    conn.close()
    
    fields_list = []
    for field in fields:
        fields_list.append({
            'id': field['id'],
            'field_name': field['field_name'],
            'field_type': field['field_type'],
            'is_required': bool(field['is_required']),
            'dropdown_options': field['dropdown_options'].split(',') if field['dropdown_options'] else []
        })
    
    return fields_list

@app.post("/api/fields")
async def add_field(field: FieldConfig):
    """Add a new field configuration"""
    conn = get_db()
    c = conn.cursor()
    
    try:
        dropdown_options = ','.join(field.dropdown_options) if field.dropdown_options else None
        c.execute('''INSERT INTO field_config (field_name, field_type, is_required, dropdown_options)
                     VALUES (?, ?, ?, ?)''',
                  (field.field_name, field.field_type, field.is_required, dropdown_options))
        conn.commit()
        conn.close()
        
        return {'success': True, 'message': 'Field added successfully'}
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(status_code=400, detail='Field already exists')

@app.delete("/api/fields/{field_id}")
async def delete_field(field_id: int):
    """Delete a field configuration"""
    conn = get_db()
    c = conn.cursor()
    c.execute('DELETE FROM field_config WHERE id = ?', (field_id,))
    conn.commit()
    conn.close()
    
    return {'success': True, 'message': 'Field deleted'}

# ============ MACHINE RECORDS ENDPOINTS ============

@app.get("/api/machines", response_model=List[MachineResponse])
async def get_machines():
    """Get all machine records"""
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM machine_records ORDER BY created_at DESC')
    records = c.fetchall()
    conn.close()
    
    machines = []
    for record in records:
        machines.append({
            'id': record['id'],
            'data': json.loads(record['record_data']),
            'created_at': record['created_at'],
            'updated_at': record['updated_at']
        })
    
    return machines

@app.post("/api/machines")
async def create_machine(machine_data: dict):
    """Create a new machine record"""
    conn = get_db()
    c = conn.cursor()
    
    now = datetime.now().isoformat()
    c.execute('''INSERT INTO machine_records (record_data, created_at, updated_at)
                 VALUES (?, ?, ?)''',
              (json.dumps(machine_data), now, now))
    conn.commit()
    
    machine_id = c.lastrowid
    conn.close()
    
    return {'success': True, 'id': machine_id}

@app.get("/api/machines/{machine_id}", response_model=MachineResponse)
async def get_machine(machine_id: int):
    """Get a specific machine record"""
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM machine_records WHERE id = ?', (machine_id,))
    record = c.fetchone()
    conn.close()
    
    if not record:
        raise HTTPException(status_code=404, detail='Machine not found')
    
    return {
        'id': record['id'],
        'data': json.loads(record['record_data']),
        'created_at': record['created_at'],
        'updated_at': record['updated_at']
    }

@app.put("/api/machines/{machine_id}")
async def update_machine(machine_id: int, machine_data: dict):
    """Update a machine record"""
    conn = get_db()
    c = conn.cursor()
    
    now = datetime.now().isoformat()
    c.execute('''UPDATE machine_records SET record_data = ?, updated_at = ?
                 WHERE id = ?''',
              (json.dumps(machine_data), now, machine_id))
    conn.commit()
    conn.close()
    
    return {'success': True, 'message': 'Machine updated successfully'}

@app.delete("/api/machines/{machine_id}")
async def delete_machine(machine_id: int):
    """Delete a machine record"""
    conn = get_db()
    c = conn.cursor()
    c.execute('DELETE FROM machine_records WHERE id = ?', (machine_id,))
    conn.commit()
    conn.close()
    
    return {'success': True, 'message': 'Machine deleted successfully'}

# ============ ML PREDICTION ENDPOINT ============

@app.post("/api/predict", response_model=PredictionResponse)
async def predict(machine_data: dict):
    """Run ML prediction on machine data"""
    try:
        # Extract features for prediction
        features = {
            'Temperature': float(machine_data.get('Temperature', 0)),
            'Pressure': float(machine_data.get('Pressure', 0)),
            'Vibration': machine_data.get('Vibration', 'Low')
        }
        
        # Get prediction from ML model
        risk_level = predict_risk(features)
        
        return {
            'success': True,
            'risk_level': risk_level,
            'features_used': features
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ============ STARTUP ============

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()
    print("✓ Database initialized")
    print("✓ API running on http://127.0.0.1:8000")
    print("✓ API docs available at http://127.0.0.1:8000/docs")

# Health check endpoint
@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {'status': 'healthy', 'service': 'Machine Data Management API'}

if __name__ == '__main__':
    import uvicorn
    init_db()
    uvicorn.run(app, host="127.0.0.1", port=8000)
