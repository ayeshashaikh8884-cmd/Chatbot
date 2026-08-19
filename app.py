"""
Flask Chatbot using Ollama (llama3.2:latest)
Topic  : KLE BCA Belgaum College Admissions
Folder : session3/
Files  : app.py, templates/index.html, data.json

Prerequisites:
  1. Install Ollama:        https://ollama.com/download
  2. Pull the model:        ollama pull llama3.2:latest
  3. Make sure Ollama server is running (it auto-runs on port 11434,
     or start manually with:  ollama serve)
  4. Install python deps:   pip install flask requests
  5. Run this app:          python app.py
  6. Open in browser:       http://127.0.0.1:5000
"""

import json
import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# ----------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "llama3.2:latest"
DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")


# ----------------------------------------------------------------------
# Load knowledge base (KLE BCA Belgaum admissions data)
# ----------------------------------------------------------------------
def load_knowledge_base():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[WARN] Could not load data.json: {e}")
        return {}


KNOWLEDGE_BASE = load_knowledge_base()


def build_system_prompt():
    """
    Builds a system prompt that grounds the LLM's answers in the
    college's admission data stored in data.json.
    """
    kb_text = json.dumps(KNOWLEDGE_BASE, indent=2)
    system_prompt = f"""
You are "KLE BCA Assist", a helpful admissions chatbot for KLE Society's
BCA (Bachelor of Computer Applications) program in Belgaum, Karnataka.

Use the following official college data as your primary source of truth
when answering questions about admissions, eligibility, fees, dates,
documents, and contact details. If a question is outside this data,
politely say you don't have that specific detail and suggest contacting
the college office directly.

Keep answers concise, friendly, and formatted clearly (use short
paragraphs or bullet points where helpful).

COLLEGE DATA (JSON):
{kb_text}
"""
    return system_prompt.strip()


SYSTEM_PROMPT = build_system_prompt()


# ----------------------------------------------------------------------
# Routes
# ----------------------------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").strip()

    if not user_message:
        return jsonify({"reply": "Please type a question about KLE BCA Belgaum admissions."})

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        "stream": False,
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=120)
        response.raise_for_status()
        result = response.json()
        reply = result.get("message", {}).get("content", "").strip()

        if not reply:
            reply = "Sorry, I couldn't generate a response. Please try again."

    except requests.exceptions.ConnectionError:
        reply = (
            "⚠️ Could not connect to Ollama. Make sure Ollama is running "
            "(run 'ollama serve') and that the model 'llama3.2:latest' "
            "is pulled ('ollama pull llama3.2:latest')."
        )
    except Exception as e:
        reply = f"⚠️ An error occurred while contacting the model: {e}"

    return jsonify({"reply": reply})


@app.route("/reset-info")
def reset_info():
    """Optional endpoint to view the raw knowledge base (for debugging)."""
    return jsonify(KNOWLEDGE_BASE)


# ----------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)