import csv
import os
from datetime import datetime

FEEDBACK_FILE = "feedback.csv"

def save_feedback(original_label, corrected_label, method, fallback_used, raw_text):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_exists = os.path.exists(FEEDBACK_FILE)
    
    with open(FEEDBACK_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not log_exists:
            writer.writerow(["timestamp", "original_label", "corrected_label", "method", "fallback_used", "preview"])
        
        # Store only preview text to avoid logging full email bodies
        writer.writerow([
            timestamp,
            original_label,
            corrected_label,
            method,
            fallback_used,
            raw_text[:300]  # 300-char preview for audit log
        ])
