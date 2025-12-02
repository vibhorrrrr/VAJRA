# ⚖️ VAJRA: Virtual Assistant for Justice, Rights, and Accountability

> **Your AI-Powered Legal Companion for the New Criminal Laws: BNS, BNSS, and BSA**

![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-success)

## 📖 Overview

**VAJRA** (Virtual Assistant for Justice, Rights, and Accountability) is an advanced AI-driven legal assistant designed to demystify India's new criminal laws:
*   **Bharatiya Nyaya Sanhita (BNS)**
*   **Bharatiya Nagarik Suraksha Sanhita (BNSS)**
*   **Bharatiya Sakshya Adhiniyam (BSA)**

Whether you are a legal professional, a student, or a citizen seeking to understand your rights, VAJRA provides accurate, instant, and easy-to-understand legal information.

VAJRA is available in two powerful formats:
1.  **💻 CLI (Command Line Interface)**: For quick, distraction-free desktop access.
2.  **📱 WhatsApp Bot**: For on-the-go legal assistance directly on your phone.

---

## ✨ Key Features

-   **🏛️ Deep Legal Expertise**: Specifically trained on the BNS, BNSS, and BSA to provide relevant and up-to-date legal information.
-   **🔍 Smart Semantic Search**: Uses FAISS vector search to find the most relevant legal sections, even if you don't use exact legal terminology.
-   **🧠 AI-Powered Explanations**: Powered by Google's Gemini AI to translate complex legal jargon into plain, understandable English.
-   **📚 Precise Citations**: Every answer is backed by specific section references from the BNS, ensuring credibility.
-   **💬 Natural Conversation**: Interact naturally—ask follow-up questions and get context-aware responses.

---

## 🛠️ Tech Stack

-   **Language**: Python 3.7+
-   **AI Model**: Google Gemini (Generative AI)
-   **Vector Database**: FAISS (Facebook AI Similarity Search)
-   **Web Framework**: Flask (for the WhatsApp webhook)
-   **Messaging Integration**: Twilio API (for WhatsApp)

---

## 🚀 Installation & Setup

### Prerequisites
-   Python 3.7 or higher installed.
-   A Google Gemini API Key.
-   (Optional) A Twilio account for WhatsApp integration.

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/vajra-chatbot.git
cd vajra-chatbot
```

### 2. Install Dependencies
The setup script will automatically install all required packages.
```bash
# Windows
python setup_cli.py

# Linux/Mac
python3 setup_cli.py
```

---

## 💻 Usage

### Option A: Command Line Interface (CLI)
The CLI is the fastest way to test and use VAJRA locally.

**Windows:**
Double-click `start_vajra.bat` or run:
```bash
start_vajra.bat
```

**Linux/Mac:**
```bash
python3 run_cli.py
```

**Commands:**
-   `search <query>`: Find relevant legal sections.
-   `sections`: Check the number of loaded sections.
-   `clear`: Clear the screen.
-   `quit` / `exit`: Close the application.

### Option B: WhatsApp Bot
To run VAJRA as a WhatsApp bot, you need to set up a local server and expose it to the internet (e.g., using ngrok).

1.  **Start the Flask Server:**
    ```bash
    python app.py
    ```
2.  **Expose Localhost (using ngrok):**
    ```bash
    ngrok http 5000
    ```
3.  **Configure Twilio:**
    -   Copy the ngrok URL (e.g., `https://your-url.ngrok.io/whatsapp`).
    -   Paste it into your Twilio Sandbox "When a message comes in" webhook field.

4.  **Chat:**
    -   Send a message to your Twilio Sandbox number to start chatting with VAJRA!

---

## 📂 Project Structure

```
vajra-chatbot/
├── 📄 app.py              # Flask application for WhatsApp bot
├── 📄 run_cli.py          # Entry point for the CLI
├── 📄 setup_cli.py        # Setup script for dependencies and data
├── 📄 start_vajra.bat     # Windows batch file for easy start
├── 📄 requirements.txt    # Python dependencies
├── 📂 backend/            # Core logic
│   ├── 📄 cli_agent.py    # Main agent logic (RAG pipeline)
│   └── 📄 embed.py        # Embedding generation utilities
└── 📂 data/               # Data storage
    ├── 📄 bns_data.json   # Legal text data
    └── 📄 bns_index.faiss # Vector index for fast searching
```

---

## 🤝 Contributing

Contributions are welcome! If you'd like to improve VAJRA, please:
1.  Fork the repository.
2.  Create a feature branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4.  Push to the branch (`git push origin feature/AmazingFeature`).
5.  Open a Pull Request.

---

## 📜 Disclaimer

> **Note:** VAJRA provides information for educational and informational purposes only. It is not a substitute for professional legal advice. Always consult with a qualified attorney for specific legal matters.

---

Made with ❤️ for Justice and Rights.
