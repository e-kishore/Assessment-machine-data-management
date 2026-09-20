"""
Simple Machine Learning Model for Risk Prediction
Using a pre-trained simple decision logic
"""

import pickle
import os
from sklearn.ensemble import RandomForestClassifier
import numpy as np

MODEL_PATH = 'risk_model.pkl'

def create_and_save_model():
    """Create and save a simple ML model"""
    
    # Training data: Temperature, Pressure, Vibration (0=Low, 1=Medium, 2=High)
    X_train = np.array([
        [30, 80, 0],   # Low temp, Low pressure, Low vibration = Low Risk
        [50, 100, 1],  # Med temp, Med pressure, Med vibration = Medium Risk
        [85, 130, 2],  # High temp, High pressure, High vibration = High Risk
        [25, 75, 0],   # Low Risk
        [60, 110, 2],  # High Risk
        [40, 90, 1],   # Medium Risk
        [90, 140, 2],  # High Risk
        [35, 85, 0],   # Low Risk
        [70, 120, 2],  # High Risk
        [45, 95, 1],   # Medium Risk
        [55, 105, 1],  # Medium Risk
        [80, 125, 2],  # High Risk
        [30, 80, 0],   # Low Risk
        [75, 115, 2],  # High Risk
        [50, 100, 1],  # Medium Risk
    ])
    
    # Labels: 0=Low Risk, 1=Medium Risk, 2=High Risk
    y_train = np.array([0, 1, 2, 0, 2, 1, 2, 0, 2, 1, 1, 2, 0, 2, 1])
    
    # Create and train Random Forest model
    model = RandomForestClassifier(n_estimators=10, random_state=42)
    model.fit(X_train, y_train)
    
    # Save model
    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(model, f)
    
    print("Model created and saved successfully!")

def load_model():
    """Load the trained model"""
    if not os.path.exists(MODEL_PATH):
        create_and_save_model()
    
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    
    return model

def convert_vibration_to_number(vibration):
    """Convert vibration text to number"""
    vibration_map = {
        'Low': 0,
        'Medium': 1,
        'High': 2
    }
    return vibration_map.get(vibration, 0)

def convert_prediction_to_label(prediction):
    """Convert prediction number to label"""
    risk_map = {
        0: 'Low Risk',
        1: 'Medium Risk',
        2: 'High Risk'
    }
    return risk_map.get(prediction, 'Unknown')

def predict_risk(features):
    """
    Predict risk level based on machine features
    
    Features expected:
    - Temperature: Number (e.g., 85)
    - Pressure: Number (e.g., 120)
    - Vibration: String (e.g., 'High')
    
    Returns:
    - Risk Level: String ('Low Risk', 'Medium Risk', 'High Risk')
    """
    
    # Load model
    model = load_model()
    
    # Convert features to model format
    temperature = float(features.get('Temperature', 50))
    pressure = float(features.get('Pressure', 100))
    vibration = convert_vibration_to_number(features.get('Vibration', 'Low'))
    
    # Create feature array
    X = np.array([[temperature, pressure, vibration]])
    
    # Make prediction
    prediction = model.predict(X)[0]
    
    # Convert to label
    risk_level = convert_prediction_to_label(prediction)
    
    return risk_level

if __name__ == '__main__':
    # Create model when script is run directly
    create_and_save_model()
    
    # Test prediction
    test_features = {
        'Temperature': 85,
        'Pressure': 120,
        'Vibration': 'High'
    }
    
    result = predict_risk(test_features)
    print(f"Test Prediction: {result}")
