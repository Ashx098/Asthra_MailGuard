import joblib
import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from asthra_mailguard.cleaner import clean_email

MODEL_PATH = "asthra_model.pkl"

def train_model(data_path):
    df = pd.read_csv(data_path)

    # Normalize column names
    df.columns = [col.strip().lower() for col in df.columns]

    # Use 'snippet' as input and 'category' as label
    if 'snippet' not in df.columns or 'category' not in df.columns:
        print("[❌] Required columns 'snippet' and 'category' not found.")
        return

    df = df[['snippet', 'category']].dropna()
    df['clean_text'] = df['snippet'].apply(clean_email)
    df = df.dropna(subset=['clean_text'])

    if df.empty:
        print("[⚠️] No valid emails to train on. Exiting.")
        return

    X = df['clean_text']
    y = df['category']

    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('clf', LogisticRegression(max_iter=1000))
    ])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    print("\n[📊] Classification Report:\n", classification_report(y_test, y_pred))

    decision = input("\n[❓] Save this model? (y/n): ")
    if decision.lower().strip() == 'y':
        joblib.dump(pipeline, MODEL_PATH)
        print(f"[✅] Model saved to {MODEL_PATH}")
    else:
        print("[⚠️] Model not saved.")

def load_model():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("Model not found. Train it first.")
    return joblib.load(MODEL_PATH)

def predict(text):
    model = load_model()
    clean = clean_email(text)
    if not clean:
        return "unknown", 0.0

    proba = model.predict_proba([clean])[0]
    label = model.classes_[proba.argmax()]
    confidence = proba.max()
    return label, confidence
