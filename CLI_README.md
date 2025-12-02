# Virtual Assistant for Justice, Rights, and Accountability (VAJRA) CLI - Command Line Legal Assistant

An interactive command-line interface for VAJRA, your AI-powered Virtual Assistant for Justice, Rights, and Accountability specializing in Bharatiya Nyaya Sanhita (BNS).

## Quick Start

### Windows
```bash
# Double-click start_vajra.bat or run:
start_vajra.bat
```

### Linux/Mac
```bash
# Setup (run once)
python3 setup_cli.py

# Start VAJRA
python3 run_cli.py
```

## Features

- 🏛️ **Legal Expertise**: Trained on Bharatiya Nyaya Sanhita (BNS)
- 🔍 **Smart Search**: AI-powered retrieval of relevant legal sections
- 💬 **Interactive Chat**: Natural language legal queries
- 📚 **Source Attribution**: Every answer includes specific section references
- 🎯 **Plain Language**: Complex legal concepts explained simply

## Commands

- `help` - Show available commands
- `quit/exit` - Exit the application
- `clear` - Clear the screen
- `sections` - Show number of loaded legal sections
- `search <term>` - Search for specific legal sections
- `examples` - Show example questions

## Example Questions

- "What is theft under BNS?"
- "What are the punishments for assault?"
- "Can I file a case for cybercrime?"
- "What is the difference between murder and culpable homicide?"
- "What are the rights during arrest?"
- "Is dowry harassment a crime?"

## Requirements

- Python 3.7+
- Internet connection (for AI model access)
- Required packages (auto-installed by setup):
  - google-generativeai
  - faiss-cpu
  - numpy

## Troubleshooting

### "Module not found" errors
Run the setup script:
```bash
python setup_cli.py
```

### "API key" errors
The system uses a pre-configured API key. If you encounter issues, check your internet connection.

### "Data files not found"
Make sure you're running from the vajra directory and that the data folder contains:
- `bns_data.json`
- `bns_index.faiss` (created automatically)

## Disclaimer

This is AI-generated legal information for educational purposes. Always consult a qualified lawyer for specific legal advice and representation.

## Support

For issues or questions, check that all files are in the correct directory structure:
```
vajra/
├── run_cli.py
├── setup_cli.py
├── start_vajra.bat
├── backend/
│   ├── cli_agent.py
│   ├── embed.py
│   └── requirements.txt
└── data/
    ├── bns_data.json
    └── bns_index.faiss
```