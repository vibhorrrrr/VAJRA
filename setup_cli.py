#!/usr/bin/env python3
"""
VAJRA CLI Setup Script
Run this once to set up the CLI environment
"""

import os
import sys
import json
import subprocess

def check_requirements():
    """Check if required packages are installed"""
    required_packages = [
        'google-generativeai',
        'faiss-cpu',
        'numpy'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("Installing missing packages...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing_packages)
            print("✅ Packages installed successfully")
        except subprocess.CalledProcessError:
            print("❌ Failed to install packages. Please install manually:")
            print(f"pip install {' '.join(missing_packages)}")
            return False
    else:
        print("✅ All required packages are installed")
    
    return True

def check_data_files():
    """Check if data files exist"""
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    
    # Check BNS data
    bns_data_path = os.path.join(data_dir, 'bns_data.json')
    if not os.path.exists(bns_data_path):
        print("❌ BNS data file not found")
        return False
    
    # Check FAISS index
    faiss_index_path = os.path.join(data_dir, 'bns_index.faiss')
    if not os.path.exists(faiss_index_path):
        print("⚠️ FAISS index not found. Creating embeddings...")
        return create_embeddings()
    
    print("✅ Data files found")
    return True

def create_embeddings():
    """Create FAISS embeddings if they don't exist"""
    try:
        backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
        embed_script = os.path.join(backend_dir, 'embed.py')
        
        if os.path.exists(embed_script):
            os.chdir(backend_dir)
            subprocess.check_call([sys.executable, 'embed.py'])
            print("✅ Embeddings created successfully")
            return True
        else:
            print("❌ Embedding script not found")
            return False
    except Exception as e:
        print(f"❌ Error creating embeddings: {e}")
        return False

def main():
    print("🔧 Setting up VAJRA CLI...")
    
    if not check_requirements():
        return False
    
    if not check_data_files():
        return False
    
    print("\n✅ VAJRA CLI setup complete!")
    print("Run 'python run_cli.py' to start the legal assistant")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)