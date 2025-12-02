# app.py

import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

# --- VAJRA Integration ---
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

try:
    from cli_agent import VajraCLI
except ImportError as e:
    print(f"❌ Critical Error: Could not import VajraCLI. Make sure backend path is correct.")
    print(f"Error details: {e}")
    sys.exit(1)

# --- Flask App Initialization ---
app = Flask(__name__)

# --- Load VAJRA Agent ONCE ---
print("🚀 Initializing VAJRA Agent... This may take a moment.")
backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
os.chdir(backend_dir)
vajra_agent = VajraCLI()
os.chdir('..')
print("✅ VAJRA Agent is ready and online.")


# --- Webhook for Twilio ---
@app.route("/whatsapp", methods=['POST'])
def whatsapp_reply():
    """Receives incoming messages from Twilio and replies."""
    incoming_msg = request.values.get('Body', '').strip()
    print(f"💬 Received message: '{incoming_msg}'")

    resp = MessagingResponse()

    if not incoming_msg or incoming_msg.lower() in ['hi', 'hello', 'start']:
        reply_text = (
            "Welcome to VAJRA, your AI legal assistant for BNS, BSA, and BNSS.\n\n"
            "Ask me a question like:\n"
            "-> What is the punishment for theft?\n"
            "-> What are the rights during an arrest?"
        )
    else:
        print("🤖 Generating response from VAJRA...")
        reply_text = vajra_agent.generate_response(incoming_msg)
        print("✉️ Sending response.")

    resp.message(reply_text)
    return str(resp)