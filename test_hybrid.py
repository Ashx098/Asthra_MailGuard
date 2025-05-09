from core_engine import classify_email
from asthra_mailguard.feedback import save_feedback
import time

def run_cli_tester():
    print("\n📬 Asthra MailGuard – CLI Tester\n" + "-"*40)

    while True:
        sender = input("\n✉️  Enter sender email (or 'q' to quit): ")
        if sender.lower() == 'q':
            break

        email_text = input("📝 Paste the email content: ")

        print("\n🤖 Classifying...")
        time.sleep(0.5)
        label = classify_email(sender, email_text)

        print(f"\n✅ Final Predicted Label: {label}")

        correct = input("🔁 Do you want to correct the label? (y/n): ").strip().lower()
        if correct == 'y':
            new_label = input("✍️  Enter the correct label: ").strip()
            method = "RULE" if "@"+sender.split('@')[-1] in open("domain_rules.json").read() else "LLM" if "LLM" in label else "ML"
            fallback_used = (method == "LLM")
            save_feedback(label, new_label, method, fallback_used, email_text)
            print("🧠 Correction saved to feedback.csv!")

        cont = input("\n🔄 Test another email? (y/n): ").strip().lower()
        if cont != 'y':
            break

    print("\n🧠 Exiting CLI Tester. Stay sharp, Chief!\n")

if __name__ == "__main__":
    run_cli_tester()
