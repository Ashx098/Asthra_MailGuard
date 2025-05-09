import csv
from datetime import datetime
import os

LOG_FILE = "predictions_log.csv"

def log_prediction(method, label, confidence, fallback_used, raw_text):
    log_exists = os.path.exists(LOG_FILE)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    preview = raw_text[:100].replace('\n', ' ').strip()

    row = [timestamp, method, label, round(confidence, 3), fallback_used, preview]

    with open(LOG_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not log_exists:
            writer.writerow(["timestamp", "method", "label", "confidence", "fallback_used", "text_preview"])
        writer.writerow(row)
