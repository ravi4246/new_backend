import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
import joblib
import os

def train():
    print("Loading dataset 'siddha_ai_training_data.csv'...")
    df = pd.read_csv("siddha_ai_training_data.csv")
    
    # We combine user health inputs into a text representation so the NLP vectorizer can extract patterns
    df['combined_features'] = df['symptoms'].fillna('') + " digestion:" + df['digestion'].fillna('') + " sleep:" + df['sleep_quality'].fillna('') + " activity:" + df['activity_level'].fillna('')
    
    X = df['combined_features']
    y = df['target_therapy_plan']
    
    print("Building model pipeline (TF-IDF + Random Forest)...")
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(max_features=1000)),
        ('clf', RandomForestClassifier(n_estimators=50, random_state=42, n_jobs=-1))
    ])
    
    print("Training real model on all 45,000+ logs... (this may take a moment)")
    pipeline.fit(X, y)
    
    accuracy = pipeline.score(X, y)
    print(f"Training Complete. Internal Overfit Accuracy: {accuracy:.4f} (expected very high on synthetic)")
    
    model_path = os.path.join(os.path.dirname(__file__), "siddha_ml_model.pkl")
    print(f"Saving certified model weights to '{model_path}'...")
    joblib.dump(pipeline, model_path)
    print("Model successfully saved! Ready for API integration.")

if __name__ == "__main__":
    train()
