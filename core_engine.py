from asthra_mailguard.model import predict
from asthra_mailguard.fallback_llm import fallback_predict
from asthra_mailguard.logger import log_prediction
from asthra_mailguard.cleaner import clean_email
import json
import re
from dotenv import load_dotenv
import os

load_dotenv()
CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", "0.6"))
SAFE_MODE = os.getenv("SAFE_MODE", "True") == "True"

DOMAIN_RULES_PATH = "domain_rules.json"

# 🔒 Safe Mode Config
from dotenv import load_dotenv
import os

SAFE_MODE = os.getenv("SAFE_MODE", "True") == "True"

SENSITIVE_KEYWORDS = {
    "financial", "bank", "account", "balance", "salary", "loan", "atm", "pension", "credit", "debit",
    "result", "marks", "score", "cbse", "board exam", "10th", "12th", "percentage", "exam",
    "medical", "health", "report", "xray", "blood", "diagnosis", "prescription"
}

# Load domain rules once
try:
    with open(DOMAIN_RULES_PATH, 'r') as f:
        DOMAIN_RULES = json.load(f)
except FileNotFoundError:
    DOMAIN_RULES = {}

def extract_domain(sender):
    match = re.search(r'@([\w\.-]+)', str(sender))
    return match.group(1).lower() if match else None

def classify_email(sender, email_text):
    domain = extract_domain(sender)

    # 1️⃣ Check domain rule
    if domain in DOMAIN_RULES:
        label = DOMAIN_RULES[domain]
        print(f"[🔒 Domain Rule Applied] Label: {label} from {domain}")
        log_prediction(
            method="RULE",
            label=label,
            confidence=1.0,
            fallback_used=False,
            raw_text=email_text
        )
        return label

    # 2️⃣ Predict using ML
    label, confidence = predict(email_text)
    if confidence >= CONFIDENCE_THRESHOLD:
        print("[ML] Label:", label, "| Confidence:", round(confidence, 3))
        log_prediction("ML", label, confidence, False, email_text)
        return label

    # 3️⃣ Safe Mode Block on Sensitive Emails
    if SAFE_MODE:
        for word in SENSITIVE_KEYWORDS:
            if word in email_text.lower():
                print("[🔒 Safe Mode] LLM fallback blocked due to possible sensitive content.")
                log_prediction("BLOCKED", "unknown", 0.0, False, email_text)
                return "unknown"


    # 4️⃣ Fallback to LLM
    label = fallback_predict(email_text)
    print("[LLM Fallback] Label:", label)
    log_prediction("LLM", label, 0.0, True, email_text)
    return label

if __name__ == "__main__":
    sender = "alerts@axisbank.com"
    email_text = "Your SBI account has been credited with ₹5000."
    classify_email(sender, email_text)
    # Test with a domain rule