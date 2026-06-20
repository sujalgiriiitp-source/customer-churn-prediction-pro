import os
import sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
import joblib

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.db_manager import load_customers, log_action
from utils.config import MODEL_DIR, MODEL_PATH, FEATURE_COLUMNS

def prepare_data(df):
    """Preprocess data for modeling."""
    # Handle missing values if any
    df = df.dropna()

    # One-hot encode categorical variables
    df = pd.get_dummies(df, columns=['contract_type'])
    
    # Ensure all expected feature columns are present
    for col in FEATURE_COLUMNS:
        if col not in df.columns:
            df[col] = 0

    # Align columns to the expected order
    X = df[FEATURE_COLUMNS]
    y = df['churn']
    
    return X, y

def train_and_evaluate_models():
    """Train multiple models, evaluate them, and save the best one."""
    print("Loading data from database...")
    df = load_customers()
    if df.empty:
        print("No data found. Please generate data first.")
        return
    
    print("Preparing data...")
    X, y = prepare_data(df)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    models = {
        'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
        'Decision Tree': DecisionTreeClassifier(random_state=42),
        'Random Forest': RandomForestClassifier(random_state=42, n_estimators=100)
    }
    
    best_model_name = None
    best_model = None
    best_f1 = -1
    best_scaler = scaler
    
    results = []
    
    for name, model in models.items():
        print(f"Training {name}...")
        model.fit(X_train_scaled, y_train)
        
        y_pred = model.predict(X_test_scaled)
        y_prob = model.predict_proba(X_test_scaled)[:, 1] if hasattr(model, "predict_proba") else [0]*len(y_test)
        
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, zero_division=0)
        rec = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)
        roc = roc_auc_score(y_test, y_prob) if hasattr(model, "predict_proba") else 0
        
        results.append({
            'Model': name,
            'Accuracy': acc,
            'Precision': prec,
            'Recall': rec,
            'F1 Score': f1,
            'ROC AUC': roc
        })
        
        if f1 > best_f1:
            best_f1 = f1
            best_model_name = name
            best_model = model

    results_df = pd.DataFrame(results)
    print("\nModel Evaluation Results:")
    print(results_df)
    
    print(f"\nBest Model: {best_model_name} (F1: {best_f1:.4f})")
    
    # Save the best model and scaler
    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump({'model': best_model, 'scaler': best_scaler, 'features': FEATURE_COLUMNS}, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")
    
    log_action("Model Training", f"Trained models. Best: {best_model_name} with F1={best_f1:.4f}")
    
    return results_df

if __name__ == "__main__":
    train_and_evaluate_models()
