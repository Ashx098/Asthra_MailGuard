import re
import string
import csv
from langdetect import detect
from nltk.corpus import stopwords
from datetime import datetime
import os

stop_words = set(stopwords.words('english'))

SKIP_LOG_FILE = "skipped_emails.csv"

def is_english(text):
    try:
        return detect(text) == 'en'
    except:
        return False

def log_skipped_email(text, reason="Non-English"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_exists = os.path.exists(SKIP_LOG_FILE)

    with open(SKIP_LOG_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not log_exists:
            writer.writerow(["timestamp", "reason", "text"])
        writer.writerow([timestamp, reason, text[:300]])  # log a preview only

def clean_email(text):
    if not is_english(text):
        log_skipped_email(text)
        return None

    # Remove HTML tags
    text = re.sub(r'<.*?>', ' ', text)

    # Remove URLs
    text = re.sub(r'http\S+|www\S+', '', text)

    # Lowercase
    text = text.lower()

    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))

    # Remove numbers
    text = re.sub(r'\d+', '', text)

    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    # Remove stopwords
    words = text.split()
    filtered_words = [word for word in words if word not in stop_words]
    
    return ' '.join(filtered_words)
