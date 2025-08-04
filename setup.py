#!/usr/bin/env python3
"""
Setup script for the YouTube Playlist Q&A Generation System.
This helps users install dependencies and configure the system.
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required Python packages."""
    print("📦 Installing required packages...")
    
    requirements = [
        "openai",
        "requests",
        "urllib3"
    ]
    
    for package in requirements:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ Installed {package}")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {package}")
            return False
    
    return True

def check_openai_key():
    """Check if OpenAI API key is set."""
    if os.getenv("OPENAI_API_KEY"):
        print("✅ OpenAI API key is set")
        return True
    else:
        print("❌ OpenAI API key not found")
        print("\nTo set your OpenAI API key:")
        print("1. Get your API key from https://platform.openai.com/api-keys")
        print("2. Set it as an environment variable:")
        print("   export OPENAI_API_KEY='your-api-key-here'")
        print("   # Or on Windows:")
        print("   set OPENAI_API_KEY=your-api-key-here")
        return False

def create_sample_structure():
    """Create sample folder structure."""
    print("\n📁 Creating sample folder structure...")
    
    folders = [
        "transcripts",
        "transcripts/PL-bndkJaV8A5VmrwvxMw-IYgSJLlV-vjH",
        "transcripts/PL-bndkJaV8A7FiNCukanBSpxK3lIFG2KK"
    ]
    
    for folder in folders:
        try:
            os.makedirs(folder, exist_ok=True)
            print(f"✅ Created {folder}/")
        except Exception as e:
            print(f"❌ Failed to create {folder}: {e}")

def main():
    """Main setup function."""
    print("🚀 YouTube Playlist Q&A Generation System Setup")
    print("=" * 50)
    
    # Install requirements
    if not install_requirements():
        print("❌ Setup failed during package installation")
        return
    
    # Check OpenAI key
    if not check_openai_key():
        print("⚠️  Please set your OpenAI API key before using the system")
    
    # Create folder structure
    create_sample_structure()
    
    print("\n✅ Setup completed!")
    print("\n📋 Next steps:")
    print("1. Set your OpenAI API key (if not already done)")
    print("2. Add transcript files to the transcripts/PL_xxx/ folders")
    print("3. Run the system:")
    print("   python main.py")
    print("   # Or for interactive mode:")
    print("   python generate_qas_from_transcripts.py")
    print("   # Or for a simple example:")
    print("   python example_usage.py")

if __name__ == "__main__":
    main() 