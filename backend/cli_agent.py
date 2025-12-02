#!/usr/bin/env python3
"""
VAJRA CLI Agent - Command Line Legal Assistant
Interactive legal assistant powered by BNS, BSA and BNSS
"""

import json
import faiss
import numpy as np
import google.generativeai as genai
import os
import sys
from datetime import datetime

class VajraCLI:
    def __init__(self):
        self.setup_api()
        self.load_data()
        self.welcome_message()
    
    def setup_api(self):
        """Configure Google Generative AI"""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        # This makes the app stop if the key is missing, which is good.
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)
        
    def load_data(self):
        """Load BNS + BSA + BNSS data and FAISS indices"""
        try:
            # Get the directory of this script
            script_dir = os.path.dirname(os.path.abspath(__file__))
            data_dir = os.path.join(script_dir, "..", "data")
            
            # Load BNS
            with open(os.path.join(data_dir, "bns_data.json"), "r", encoding="utf-8") as f:
                self.bns_entries = json.load(f)
            self.bns_index = faiss.read_index(os.path.join(data_dir, "bns_index.faiss"))
            print(f"📚 Loaded {len(self.bns_entries)} BNS sections")

            # Load BSA
            with open(os.path.join(data_dir, "bsa_data.json"), "r", encoding="utf-8") as f:
                self.bsa_entries = json.load(f)
            self.bsa_index = faiss.read_index(os.path.join(data_dir, "bsa_index.faiss"))
            print(f"📚 Loaded {len(self.bsa_entries)} BSA sections")

            # Load BNSS
            with open(os.path.join(data_dir, "bnss_data.json"), "r", encoding="utf-8") as f:    
                self.bnss_entries = json.load(f)
            self.bnss_index = faiss.read_index(os.path.join(data_dir, "bnss_index.faiss"))
            print(f"📚 Loaded {len(self.bnss_entries)} BNSS sections")

        except FileNotFoundError as e:
            print(f"❌ Error loading data: {e}")
            print("Make sure the data files exist in the data directory")
            sys.exit(1)

    def embed_text(self, text):
        """Generate embedding for text using Google's model"""
        try:
            emb = genai.embed_content(
                model="models/text-embedding-004",
                content=text
            )["embedding"]
            return np.array(emb, dtype="float32")
        except Exception as e:
            print(f"❌ Embedding error: {e}")
            return None 
    
    def search_bns(self, query, k=3):
        """Search for relevant BNS sections"""
        q_emb = self.embed_text(query)
        if q_emb is None:
            return []
        
        q_emb = q_emb.reshape(1, -1)
        distances, indices = self.bns_index.search(q_emb, k)

        results = []
        for i, idx in enumerate(indices[0]):
            if idx < len(self.bns_entries):
                entry = self.bns_entries[idx].copy()
                entry['relevance_score'] = float(distances[0][i])
                results.append(entry)
        return results

    def search_bsa(self, query, k=3):
        """Search for relevant BSA sections"""
        q_emb = self.embed_text(query)
        if q_emb is None:
            return []
        
        q_emb = q_emb.reshape(1, -1)
        distances, indices = self.bsa_index.search(q_emb, k)
        
        results = []
        for i, idx in enumerate(indices[0]):
            if idx < len(self.bsa_entries):
                entry = self.bsa_entries[idx].copy()
                entry['relevance_score'] = float(distances[0][i])
                results.append(entry)
        return results

    def search_bnss(self, query, k=3):
        """Search for relevant BNSS sections"""
        q_emb = self.embed_text(query)
        if q_emb is None:
            return []
        
        q_emb = q_emb.reshape(1, -1)
        distances, indices = self.bnss_index.search(q_emb, k)
        
        results = []
        for i, idx in enumerate(indices[0]):
            if idx < len(self.bnss_entries):
                entry = self.bnss_entries[idx].copy()
                entry['relevance_score'] = float(distances[0][i])
                results.append(entry)
        return results

    def generate_response(self, query):
        """Generate legal response using RAG from BNS + BSA + BNSS"""
        print("🔍 Searching relevant legal sections...")
        
        # Search across multiple sources
        bns_context = self.search_bns(query, k=3)
        bsa_context = self.search_bsa(query, k=3)
        bnss_context = self.search_bnss(query, k=3)
        
        if not (bns_context or bsa_context or bnss_context):
            return "❌ Sorry, I couldn't find relevant legal information for your query."
        
        # Build combined context text
        context_text = ""
        if bns_context:
            context_text += "BNS Context:\n"
            context_text += "\n".join([
                f"Section {c['section_number']} - {c['section_title']}: {c['description']}"
                for c in bns_context
            ]) + "\n\n"
        if bsa_context:
            context_text += "BSA Context:\n"
            context_text += "\n".join([
                f"Section {c['section_number']} - {c['section_title']}: {c['description']}"
                for c in bsa_context
            ]) + "\n\n"
        if bnss_context:
            context_text += "BNSS Context:\n"
            context_text += "\n".join([
                f"Section {c['section_number']} - {c['section_title']}: {c['description']}"
                for c in bnss_context
            ]) + "\n\n"
        
        # Create prompt
        prompt = f"""You are VAJRA (Virtual Assistant for Justice, Rights, and Accountability), 
a legal assistant trained on:
- Bharatiya Nyaya Sanhita (BNS)
- Bharatiya Sakshya Adhiniyam (BSA)
- Bharatiya Nagarik Suraksha Sanhita (BNSS)

Context from law databases:
{context_text}

User Question: {query}

Instructions:
- Always answer in plain text (no bold, no markdown, use bullet points if necessary).
- Mention section numbers and specify whether they belong to BNS, BSA, or BNSS.
- Explain legal concepts in clear, simple language with examples if helpful.
- If the question is outside these laws, state that clearly.
- Always remind the user this is general information only and they should consult a qualified lawyer.
- If the query is urgent, provide the most relevant helpline numbers:
  Police / Emergency: 100
  Women’s Helpline: 1091
  NCW WhatsApp: 7827170170
  Childline: 1098
  Cyber Crime Helpline: 1930
  Legal Aid (NALSA): 15100
  Ambulance: 102 or 108
- The LLM must handle queries in multiple languages and respond in the same language.
- Provide comparative insights where relevant (old IPC/CrPC/Evidence Act vs new BNS/BNSS/BSA).
- Provide historical context and reasons for introduction of new laws.
- Handle hypothetical scenarios, always with the disclaimer this is not legal advice.
- Recognize and respond to queries about related legal concepts (Constitution, SC judgments, etc).
- Mention implementation status of the new laws and public debates if relevant.

Answer:"""
        
        print("🤖 Generating response...")
        try:
            model = genai.GenerativeModel('gemini-2.0-flash-lite')
            response = model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.2,
                    max_output_tokens=300
                )
            )
            return response.text
        except Exception as e:
            return f"❌ Error generating response: {e}"
    
    def welcome_message(self):
        """Display welcome message"""
        print("\n" + "="*60)
        print("🏛️  VAJRA - AI-Powered Virtual Assistant for Justice, Rights, and Accountability")
        print("📖 BNS + BSA + BNSS Expert")
        print("="*60)
        print("Ask me any legal question related to Indian criminal law!")
        print("Type 'help' for commands, 'quit' to exit")
        print("-"*60)
    
    def show_help(self):
        """Show available commands"""
        help_text = """
Available commands:
• help          - Show this help message
• quit/exit     - Exit the application
• clear         - Clear the screen
• sections      - Show number of loaded sections
• search <term> - Search for specific legal sections
• examples      - Show example questions

Just type your legal question to get an answer!
        """
        print(help_text)
    
    def show_examples(self):
        """Show example questions"""
        examples = [
            "What is theft under BNS?",
            "What are the punishments for assault?",
            "Can I file a case for cybercrime?",
            "What is the difference between murder and culpable homicide?",
            "What are the rights during arrest?",
            "Is dowry harassment a crime?"
        ]
        print("\n📝 Example questions you can ask:")
        for i, example in enumerate(examples, 1):
            print(f"{i}. {example}")
        print()
    
    def search_sections(self, term):
        """Search for sections containing specific terms in BNS"""
        matching_sections = []
        term_lower = term.lower()
        
        for entry in self.bns_entries:
            if (term_lower in entry['section_title'].lower() or 
                term_lower in entry['description'].lower()):
                matching_sections.append(entry)
        
        if matching_sections:
            print(f"\n🔍 Found {len(matching_sections)} BNS sections matching '{term}':")
            for section in matching_sections[:5]:  # Show first 5
                print(f"\n📋 {section['section_number']} - {section['section_title']}")
                print(f"   {section['description'][:200]}...")
        else:
            print(f"❌ No sections found matching '{term}'")
    
    def run(self):
        """Main CLI loop"""
        while True:
            try:
                user_input = input("\n💬 Ask VAJRA: ").strip()
                
                if not user_input:
                    continue
                
                # Handle commands
                if user_input.lower() in ['quit', 'exit']:
                    print("👋 Thank you for using VAJRA! Stay legally informed!")
                    break
                elif user_input.lower() == 'help':
                    self.show_help()
                elif user_input.lower() == 'clear':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    self.welcome_message()
                elif user_input.lower() == 'sections':
                    print(f"📚 Loaded {len(self.bns_entries)} BNS sections")
                    print(f"📚 Loaded {len(self.bsa_entries)} BSA sections")
                    print(f"📚 Loaded {len(self.bnss_entries)} BNSS sections")
                elif user_input.lower() == 'examples':
                    self.show_examples()
                elif user_input.lower().startswith('search '):
                    search_term = user_input[7:].strip()
                    if search_term:
                        self.search_sections(search_term)
                    else:
                        print("❌ Please provide a search term")
                else:
                    # Generate legal response
                    print(f"\n⏰ {datetime.now().strftime('%H:%M:%S')} - Processing your query...")
                    response = self.generate_response(user_input)
                    print(f"\n🏛️ VAJRA's Response:")
                    print("-" * 50)
                    print(response)
                    print("-" * 50)
                    print("⚖️ Disclaimer: This is AI-generated legal information. Consult a qualified lawyer for specific legal advice.")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye! Use 'quit' to exit properly next time.")
                break
            except Exception as e:
                print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    try:
        vajra = VajraCLI()
        vajra.run()
    except Exception as e:
        print(f"❌ Failed to start VAJRA: {e}")
        sys.exit(1)



