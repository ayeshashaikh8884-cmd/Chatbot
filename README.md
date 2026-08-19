# 🎓 KLE BCA Assist – College Admissions Chatbot

KLE BCA Assist is a Flask-based chatbot that answers questions about
admissions to **K.L.E. Society's Bachelor of Computer Applications (BCA)
College, Belgaum**. It uses a local LLM ([Ollama](https://ollama.com) running
`llama3.2:latest`) grounded in a custom knowledge base (`data.json`) covering
eligibility, admission process, fees, scholarships, and facilities.

---

## ✨ Features

- 💬 Simple, clean chat interface built for prospective students
- 🎓 Answers grounded in a dedicated college admissions knowledge base
  (`data.json`) — eligibility, admission steps, required documents, fees,
  scholarships, facilities, placements, and FAQs
- 🧠 Short conversational memory within a session (via Flask session) so
  follow-up questions retain context
- 🎨 UI built entirely with **Bootstrap 5** (via CDN) — no custom CSS/JS files
- 🔄 "Reset Chat" button to start a fresh conversation
- 🤖 Powered by a locally running **Ollama** model (`llama3.2:latest`)
- ⚠️ Falls back to advising users to contact the admission office directly
  when a question isn't covered by the knowledge base, instead of guessing

---

## 📁 Project Structure

```
session3/
├── app.py               # Flask backend (routes, session memory, Ollama calls)
├── data.json             # KLE BCA Belgaum admissions knowledge base
└── templates/
    └── index.html               # Bootstrap-only chat UI
```

---

## 🧰 Prerequisites

- Python 3.8 or higher
- [Ollama](https://ollama.com/download) installed and running locally
- The `llama3.2:latest` model pulled in Ollama

---

## 🚀 Local Setup & Run

1. **Clone or download** this project into a folder named `session3`.

2. **Install Python dependencies:**
   ```bash
   pip install flask requests
   ```

3. **Install Ollama** (if not already installed):
   [https://ollama.com/download](https://ollama.com/download)

4. **Pull the model** (one-time download):
   ```bash
   ollama pull llama3.2:latest
   ```

5. **Start the Ollama server** (if it isn't already running in the background):
   ```bash
   ollama serve
   ```

6. **Run the Flask app:**
   ```bash
   python app.py
   ```

7. **Open the app** in your browser:
   ```
   http://127.0.0.1:5000
   ```

8. Start typing your admission-related questions in the chat window — e.g.
   *"What is the eligibility for BCA?"* or *"What documents do I need for
   admission?"*

---

## 🧠 How It Works

- `data.json` holds structured information about the college: eligibility
  criteria, admission process & required documents, fee details,
  scholarships, facilities, placement info, and common FAQs.
- On startup, `app.py` loads this JSON and embeds it into a **system
  prompt**, instructing the model to answer only using this knowledge base
  and to direct users to the admission office for anything not covered.
- Each visitor's conversation is kept in the Flask `session` (cookie-based),
  capped at the last 20 messages, so replies stay contextual without
  growing unbounded.
- The `/api/chat` endpoint sends the system prompt + conversation history to
  Ollama's `/api/chat` endpoint and returns the model's reply as JSON.

---

## 🔌 API Endpoints

| Method | Endpoint      | Description                                   |
|--------|---------------|-------------------------------------------------|
| GET    | `/`           | Renders the chat UI and resets session history  |
| POST   | `/api/chat`   | Sends a user message, returns the bot's reply   |
| POST   | `/api/reset`  | Clears the current session's conversation       |

---

## ⚙️ Configuration

Environment variables (optional):

| Variable      | Default                              | Description                    |
|---------------|----------------------------------------|----------------------------------|
| `OLLAMA_URL`  | `http://localhost:11434/api/chat`     | URL of the Ollama chat endpoint |
| `OLLAMA_MODEL`| `llama3.2:latest`                     | Model name to use               |

To customize the chatbot for a different college or course, simply edit the
contents of `data.json` — the system prompt is generated automatically from
whatever is in that file.

---

## ☁️ Deploying on Render / Other Cloud Hosts

⚠️ **Important:** Render (and most standard PaaS platforms) cannot run
Ollama or host a local LLM — there is no way to install/run the Ollama
daemon or the `llama3.2` model on a typical web service plan (insufficient
RAM/disk, no persistent background process support).

To deploy the **Flask app** on a platform like Render:

### Option A — Point the app at a remote Ollama instance
Run Ollama on your own machine or a separate VPS with enough resources,
expose it securely, and set the `OLLAMA_URL` environment variable to that
public address.

### Option B — Swap Ollama for a hosted LLM API
Replace the Ollama call in `app.py` with a hosted API (e.g. Anthropic,
OpenAI, Groq) that doesn't require a locally running model server.

**Typical Render service settings** (once the model backend is sorted):

- **Build Command:**
  ```
  pip install -r requirements.txt
  ```
- **Start Command:**
  ```
  gunicorn app:app
  ```
- **Environment Variables:**
  - `OLLAMA_URL` (if using Option A)
  - Any API keys (if using Option B)
  - `SECRET_KEY` for Flask sessions in production

Remember to add a `requirements.txt` (Flask, requests, gunicorn) before
deploying.

---

## 🛠️ Tech Stack

- **Backend:** Flask (Python)
- **LLM:** Ollama (`llama3.2:latest`)
- **Frontend:** HTML + Bootstrap 5 (CDN only, no custom CSS/JS)

---

## ⚠️ Disclaimer

Fee amounts, eligibility criteria, and other admission details in
`data.json` are indicative and sourced from public information. Always
verify current admission dates, fees, and eligibility directly with the
K.L.E. Society BCA College admission office before making decisions.

---

## 📄 License

This project is provided as-is for educational/demo purposes. Feel free to
modify and extend it.
