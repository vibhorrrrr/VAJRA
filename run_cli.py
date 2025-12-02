#!/usr/bin/env python3
"""
VAJRA CLI Runner
Run this script to start the command-line legal assistant
"""

import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# Change to backend directory for relative paths to work
backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
os.chdir(backend_dir)

try:
    from cli_agent import VajraCLI
    
    print("🚀 Starting VAJRA CLI...")
    vajra = VajraCLI()
    vajra.run()
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure all dependencies are installed: pip install -r requirements.txt")
except Exception as e:
    print(f"❌ Error starting VAJRA: {e}")
    sys.exit(1)