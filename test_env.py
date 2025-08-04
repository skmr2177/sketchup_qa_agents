#!/usr/bin/env python3
"""
Test Environment Variables
==========================

Test if .env file is properly set up and API key is accessible.
"""

import os
from pathlib import Path

def test_env_file():
    """Test .env file setup"""
    
    print("🔍 Testing .env file setup...")
    
    # Check if .env file exists
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ .env file not found!")
        print("💡 Create a .env file with: OPENAI_API_KEY=your_api_key_here")
        return False
    
    print("✅ .env file found")
    
    # Read .env file content (first few lines only for security)
    try:
        with open(".env", "r") as f:
            lines = f.readlines()[:3]  # Only first 3 lines for security
        
        api_key_line = None
        for line in lines:
            if line.strip().startswith("OPENAI_API_KEY"):
                api_key_line = line.strip()
                break
        
        if api_key_line:
            print(f"✅ Found API key line in .env file")
            print(f"   Format: {api_key_line[:30]}...")
        else:
            print("❌ No OPENAI_API_KEY line found in .env file")
            return False
            
    except Exception as e:
        print(f"❌ Error reading .env file: {e}")
        return False
    
    return True

def test_env_loading():
    """Test environment variable loading"""
    
    print("\n🔄 Testing environment variable loading...")
    
    # Test without load_dotenv
    api_key_before = os.getenv("OPENAI_API_KEY")
    print(f"API key before load_dotenv: {'Found' if api_key_before else 'Not found'}")
    
    # Load environment variables
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ load_dotenv() executed successfully")
    except ImportError:
        print("❌ python-dotenv not installed! Run: pip install python-dotenv")
        return False
    except Exception as e:
        print(f"❌ Error loading .env: {e}")
        return False
    
    # Test after load_dotenv
    api_key_after = os.getenv("OPENAI_API_KEY")
    
    if api_key_after:
        print(f"✅ API key loaded successfully")
        print(f"   Key length: {len(api_key_after)} characters")
        print(f"   Key format: {api_key_after[:10]}...{api_key_after[-4:]}")
        return True
    else:
        print("❌ API key still not found after loading .env")
        return False

def test_agent_creation():
    """Test creating agents with the loaded API key"""
    
    print("\n🤖 Testing agent creation...")
    
    try:
        from agents.main import create_agents
        
        qa_generator, refiner = create_agents()
        
        print("✅ Agents created successfully!")
        print(f"   QA Generator: {qa_generator.name}")
        print(f"   Refiner: {refiner.name}")
        
        return True
        
    except Exception as e:
        print(f"❌ Agent creation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    
    print("🧪 Environment Variable Test")
    print("=" * 40)
    
    # Step 1: Test .env file
    if not test_env_file():
        return
    
    # Step 2: Test environment loading
    if not test_env_loading():
        return
    
    # Step 3: Test agent creation
    if test_agent_creation():
        print("\n🎉 SUCCESS! Everything is working!")
        print("✅ .env file is properly set up")
        print("✅ API key loads correctly")
        print("✅ Agents can be created")
    else:
        print("\n❌ Agent creation failed despite API key being loaded")

if __name__ == "__main__":
    main() 