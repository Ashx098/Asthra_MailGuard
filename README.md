# 🛡️ Asthra MailGuard

**Asthra MailGuard** is a **privacy-first, AI-powered command-line tool** that helps you classify, flag, and analyze emails — entirely on your local machine.

It uses a **self-learning hybrid engine** combining a fast Logistic Regression model with fallback to a powerful **Hermes 3 LLM** running via [Ollama](https://ollama.com).
Whether it's spam, important, or promotional — MailGuard helps you decide, learn, and adapt over time.

> ⚠️ This is an **alpha release** intended for testing, feedback, and collaborative improvements.
> 🇮🇳 Built with purpose in India by [Asthra AI](https://asthra.vercel.app)

---

## 🚀 Features

* ✅ **Local classification** of emails (Important / Spam / Promotions)
* ✅ **Hybrid ML + LLM engine** with confidence thresholding
* ✅ **Safe-mode** toggle for LLM usage
* ✅ Built-in **self-learning** from user feedback
* ✅ Structured logs, datasets, retraining pipeline
* ✅ Optional future UI support via React (`asthra-ui`)

---

## 🏗️ Project Structure

```
ASTHRA_MAILGUARD/
├── asthra_mailguard/         # Core Python backend
│   ├── model.py              # Logistic Regression classifier
│   ├── fallback_llm.py       # Hermes3 LLM fallback logic
│   ├── retrainer.py          # Self-learning (feedback-based retraining)
│   ├── cleaner.py            # Preprocessing functions
│   ├── feedback.py           # Collect and manage user feedback
│   ├── logger.py             # Token tracking and prediction logs
│   └── __init__.py
│
├── test_hybrid.py            # ✅ Main CLI entry script
├── train_classifier.py       # Model retraining script
├── gmail_fetcher.py          # Gmail API integration (optional)
│
├── asthra_model.pkl          # Pre-trained ML model
├── *.csv / *.json            # Datasets, feedback, rules, logs
├── asthra_mailguard_env/     # Python virtual environment (ignored)
├── asthra-ui/                # React-based frontend (WIP)
├── node_modules/             # Node dependencies (ignored)
├── .env                      # Environment config
├── README.md                 # Project documentation
└── assets/                   # Demo screenshots and logos
```

---

## ⚙️ Setup Instructions

### 🔹 1. Clone the Repo

```bash
git clone https://github.com/your-username/asthra-mailguard.git
cd asthra-mailguard
```

---

### 🔹 2. Install Python Dependencies

Ensure Python ≥ 3.10 is installed.

```bash
pip install -r requirements.txt
```

---

### 🔹 3. Set Up LLM (Hermes 3 via Ollama)

1. Download [Ollama](https://ollama.com/download)
2. Pull the Hermes 3 model:

```bash
ollama pull hermes:latest
```

> ℹ️ You can disable LLM fallback using `SAFE_MODE=True` in `.env`

---

### 🔹 4. Configure `.env` File

Create a `.env` file in the root with:

```env
PYTHONPATH=.
SAFE_MODE=True
CONFIDENCE_THRESHOLD=0.6
```

* `SAFE_MODE=True` → disables LLM fallback (pure ML mode)
* `CONFIDENCE_THRESHOLD=0.6` → if ML confidence is lower than this, Hermes3 LLM is used

---

## 🧪 How to Use (CLI)

### ▶️ Run the CLI tool:

```bash
python test_hybrid.py
```

### 📨 What it does:

1. Prompts you to paste **email content**
2. **Cleans and preprocesses** it
3. Uses trained ML model to classify
4. If confidence is low:

   * Fallbacks to **Hermes3 LLM**
   * Returns verdict with justification
5. Saves result and logs for feedback-based improvement

---

## 🌍 Example CLI Session

```bash
$ python test_hybrid.py

📩 Enter your email content:
> "Congratulations! You've won a free iPhone..."

📅 Prediction: Spam
🤖 Reason: ML was 51% confident → fallback to Hermes3 → Detected phishing keywords + tone

🧠 Action: Saved to log, learnable via feedback loop.
```

---

## 🖼️ Demo Screenshots

### 📩 CLI Classifier in Action

<p align="center">
  <img src="assets/res1.png" width="600"/>
</p>

### 🤖 Fallback to Hermes3 (LLM) Output

<p align="center">
  <img src="assets/res2.png" width="600"/>
</p>

---

## 📊 Datasets & Logs

* **Input datasets**:
  `emails.csv`, `emails_balanced_expanded.csv`, `emails_labeled_refined.csv`

* **Feedback & logs**:

  * `feedback.csv`: collected for retraining
  * `predictions_log.csv`: tracks outputs and LLM usage
  * `skipped_emails.csv`: for incomplete or error-prone inputs

---

## 🔀 Retraining the Model

To retrain using feedback:

```bash
python train_classifier.py
```

> It automatically pulls updated labels from `feedback.csv`.

---

## 🔐 Privacy Note

Asthra MailGuard is designed for **local use only**:

* No data is sent to cloud services
* All LLMs run via Ollama on your system
* Feedback data remains on your machine

You own your data. Always.

---

## 🛠️ Upcoming Features

* 📬 Gmail auto-fetch and auto-flagging
* 🖥️ Full React-based UI
* 📊 Email prioritization and summarization
* 📤 Smart reply suggestion engine
* 🧠 LLM fine-tuning via feedback loop

---

## 👨‍💼 Contribute

Want to improve this project?
Pull requests, issues, and discussions are welcome!

### We need:

* Frontend engineers (React, Tailwind)
* ML / LLM optimization nerds
* Real-world dataset testers
* UI/UX testers

---

## 📜 License

MIT License — use freely, build ethically.

---

## 🙌 Built by

**[MSR Avinash](https://aviinashh-ai.vercel.app)**
Founder, [Asthra AI](https://asthra.vercel.app)

> **Asthra AI** builds meaningful AI tools for real people — not just tech demos.
> 🇮🇳 Built in India. For India. For the world.

---

## 🔗 Tags

`#AsthraAI` `#MailGuard` `#Hermes3` `#OpenSource` `#Ollama` `#LLMTooling` `#StartupIndia` `#PrivacyFirstAI` `#IndiaFirst`
