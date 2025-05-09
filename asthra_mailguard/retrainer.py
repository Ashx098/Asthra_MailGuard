import pandas as pd
import os
import joblib
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from asthra_mailguard.cleaner import clean_email

FEEDBACK_FILE = "feedback.csv"
BASE_DATASET = "emails_balanced_expanded.csv"
MODEL_DIR = "asthra_mailguard/model_versions"
ARCHIVE_DIR = "asthra_mailguard/feedback_archive"
REQUIRED_FEEDBACK_ROWS = 20

def retrain_model():
    if not os.path.exists(FEEDBACK_FILE):
        print("[⚠️] No feedback.csv found.")
        return

    feedback_df = pd.read_csv(FEEDBACK_FILE)
    if len(feedback_df) < REQUIRED_FEEDBACK_ROWS:
        print(f"[ℹ️] Only {len(feedback_df)} feedback rows found. Need {REQUIRED_FEEDBACK_ROWS} to retrain.")
        return

    print("[🔁] Retraining model using feedback...")

    # Clean feedback
    feedback_df['clean_text'] = feedback_df['text'].apply(clean_email)
    feedback_df = feedback_df.dropna(subset=['clean_text'])
    feedback_data = feedback_df[['clean_text', 'corrected_label']].rename(columns={'corrected_label': 'label'})

    # Load and clean base dataset
    base_df = pd.read_csv(BASE_DATASET)
    base_df = base_df[['Snippet', 'Category']].dropna()
    base_df['clean_text'] = base_df['Snippet'].apply(clean_email)
    base_df = base_df.dropna(subset=['clean_text'])
    base_data = base_df[['clean_text', 'Category']].rename(columns={'Category': 'label'})

    # Combine & deduplicate
    all_data = pd.concat([base_data, feedback_data], ignore_index=True)
    all_data = all_data.drop_duplicates(subset=["clean_text", "label"])
    print(f"[📊] Dataset after merge + dedup: {len(all_data)} samples")

    # Optional: Balance dataset
    min_count = all_data['label'].value_counts().min()
    balanced = all_data.groupby('label').apply(lambda x: x.sample(min(len(x), min_count), random_state=42)).reset_index(drop=True)
    print(f"[⚖️] Balanced dataset to {min_count} per category")

    # Train/test split
    X = balanced['clean_text']
    y = balanced['label']
    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.2, random_state=42)

    # Train pipeline
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('clf', LogisticRegression(max_iter=1000))
    ])
    pipeline.fit(X_train, y_train)

    # Evaluate
    y_pred = pipeline.predict(X_test)
    report = classification_report(y_test, y_pred)
    print("\n[📊] Updated Model Report:\n", report)

    # Save model with versioning
    os.makedirs(MODEL_DIR, exist_ok=True)
    version = datetime.now().strftime("%Y%m%d_%H%M")
    model_path = os.path.join(MODEL_DIR, f"asthra_model_v{version}.pkl")
    joblib.dump(pipeline, model_path)
    print(f"[✅] Retrained model saved to {model_path}")

    # Archive feedback
    os.makedirs(ARCHIVE_DIR, exist_ok=True)
    archive_file = os.path.join(ARCHIVE_DIR, f"feedback_processed_{version}.csv")
    feedback_df.to_csv(archive_file, index=False)
    os.remove(FEEDBACK_FILE)
    print(f"[📦] Feedback archived → {archive_file}")

if __name__ == "__main__":
    retrain_model()
