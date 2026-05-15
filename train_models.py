import os
import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification

MODELS_DIR = os.path.join(os.path.dirname(__file__), '../models')
os.makedirs(MODELS_DIR, exist_ok=True)

def train_and_save_mock_model(name, n_features):
    print(f"Training mock model for {name} with {n_features} features...")
    # Generate random dataset
    X, y = make_classification(n_samples=1000, n_features=n_features, n_informative=n_features-1, n_redundant=1, random_state=42)
    
    # Train model
    clf = RandomForestClassifier(n_estimators=50, random_state=42)
    clf.fit(X, y)
    
    # Save model
    model_path = os.path.join(MODELS_DIR, f'{name}_model.pkl')
    joblib.dump(clf, model_path)
    print(f"Saved {model_path}")

if __name__ == "__main__":
    print("Starting mock model generation...")
    
    # Define features expected for each disease
    # Diabetes: Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age (8 features)
    train_and_save_mock_model('diabetes', 8)
    
    # Heart: age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal (13 features)
    train_and_save_mock_model('heart', 13)
    
    # Parkinsons: MDVP:Fo(Hz), MDVP:Fhi(Hz), MDVP:Flo(Hz), MDVP:Jitter(%), MDVP:Jitter(Abs), MDVP:RAP, MDVP:PPQ, Jitter:DDP, MDVP:Shimmer, MDVP:Shimmer(dB), Shimmer:APQ3, Shimmer:APQ5, MDVP:APQ, Shimmer:DDA, NHR, HNR, RPDE, DFA, spread1, spread2, D2, PPE (22 features)
    train_and_save_mock_model('parkinsons', 22)
    
    # Liver: Age, Gender, Total_Bilirubin, Direct_Bilirubin, Alkaline_Phosphotase, Alamine_Aminotransferase, Aspartate_Aminotransferase, Total_Protiens, Albumin, Albumin_and_Globulin_Ratio (10 features)
    train_and_save_mock_model('liver', 10)
    
    # Kidney: age, bp, sg, al, su, rbc, pc, pcc, ba, bgr, bu, sc, sod, pot, hemo, pcv, wc, rc, htn, dm, cad, appet, pe, ane (24 features)
    train_and_save_mock_model('kidney', 24)

    print("All models generated successfully.")
