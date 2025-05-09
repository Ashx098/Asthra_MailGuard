import requests
from asthra_mailguard.cleaner import clean_email

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "hermes3"

# Categories we allow LLM to classify into (safe)
SAFE_LABELS = [
    "job_alert",
    "education",
    "promo",
    "message",
    "social",
    "other",
    "result_notification",  # Added here
    "financial"  # Also allowed if Safe Mode is disabled
]

def call_llm(text):
    prompt = f"""
You are an intelligent inbox email classification system.  
Classify the given email into ONE of the following categories:

- job_alert → Job offers, recruiter messages, interview updates, or hiring alerts.  
- promo → Discounts, coupons, product offers, shopping deals.  
- education → Course updates, college admissions, certificates, training programs.  
- result_notification → Exam results, marks, grades, board results, score updates.  
- financial → Bank transactions, wallet alerts, salary, debit/credit messages.  
- message → Casual messages like "hi", "hello", or plain replies.  
- social → Emails from platforms like Instagram, Facebook, WhatsApp, Twitter.  
- other → Anything that doesn't fit above.

Return **only the correct category label** with no explanation.

Email:
\"\"\"
{text}
\"\"\"
"""
    try:
        response = requests.post(OLLAMA_URL, json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        })
        response.raise_for_status()
        data = response.json()
        prediction = data.get("response", "").strip().lower()

        return prediction
    except Exception as e:
        print(f"[LLM ❌] Error calling Ollama LLM: {e}")
        return "unknown"

def fallback_predict(email_text):
    clean = clean_email(email_text)
    if not clean:
        return "unknown"

    prediction = call_llm(clean)
    if prediction in SAFE_LABELS:
        return prediction
    else:
        print(f"[⚠️] LLM predicted '{prediction}', which is not in SAFE_LABELS.")
        return "unknown"
