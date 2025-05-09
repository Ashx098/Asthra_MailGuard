from asthra_mailguard.feedback import save_feedback

email_text = "You have a new job alert from TCS."
save_feedback(
    original_label="other",
    corrected_label="job_alert",
    method="LLM",
    fallback_used=True,
    text=email_text
)
