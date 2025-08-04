#!/usr/bin/env python3
"""
Automated YouTube Q&A Generation Agent
=====================================

This script provides a command-line interface for the automated YouTube Q&A generation agent.
Simply provide a YouTube playlist URL and the agent will automatically:

1. Download transcripts from all videos
2. Generate Q&A pairs using AI agents  
3. Remove duplicates using semantic similarity
4. Save results to a structured JSON file

Usage:
    python run_agent.py

Requirements:
    - OpenAI API key set in .env file
    - All dependencies installed (see requirements.txt)
"""

import os
import sys
import asyncio
from pathlib import Path

def check_requirements():
    """Check if all requirements are met before running the agent"""
    
    # Check if .env file exists
    if not Path(".env").exists():
        print("❌ Error: .env file not found!")
        print("📝 Please create a .env file with your OpenAI API key:")
        print("   OPENAI_API_KEY=your_openai_api_key_here")
        return False
    
    # Try to import required packages
    try:
        import pytube
        import youtube_transcript_api
        import sentence_transformers
        print("✅ All required packages found")
    except ImportError as e:
        print(f"❌ Error: Missing required package: {e}")
        print("📦 Please install requirements: pip install -r requirements.txt")
        return False
    
    return True

def get_playlist_url():
    """Get playlist URL from user input with validation"""
    
    print("\n🎯 YouTube Q&A Generation Agent")
    print("=" * 50)
    
    while True:
        url = input("\n📥 Enter YouTube playlist URL: ").strip()
        
        if not url:
            print("❌ Please enter a valid URL")
            continue
            
        if "youtube.com" not in url and "youtu.be" not in url:
            print("❌ Please enter a valid YouTube URL")
            continue
            
        if "list=" not in url:
            print("❌ Please enter a playlist URL (should contain 'list=')")
            continue
            
        return url

def run_agent_sync(playlist_url):
    """Run the agent asynchronously"""
    
    try:
        # Import here to avoid issues if packages aren't installed
        sys.path.append('.')
        from agents.main import run_agent_pipeline
        
        print("\n🚀 Initializing YouTube Q&A Agent...")
        print(f"🎬 Processing playlist: {playlist_url}")
        
        # Generate timestamped output filename
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"output/sketchup_qas_{timestamp}.json"
        
        # Ensure output directory exists before running pipeline
        output_dir = os.path.dirname(output_file)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        
        result = run_agent_pipeline(playlist_url, output_file=output_file)
        
        if result is None:
            print("\n❌ Pipeline failed - no transcripts available or processing error")
            return None
        
        print("\n" + "=" * 60)
        print("🎉 SUCCESS! Agent completed successfully!")
        print(f"📄 Results saved to: {result}")
        print("=" * 60)
        
        return result
        
    except Exception as e:
        print(f"\n❌ Error: Agent failed with error: {e}")
        print("\n💡 Tips:")
        print("   - Check your OpenAI API key in .env file")
        print("   - Ensure the playlist URL is correct and public")
        print("   - Check your internet connection")
        print("   - Some videos might not have transcripts available")
        return None

def show_results_summary(output_file):
    """Show a summary of the generated results"""
    
    if not output_file:
        return
        
    # Check if file actually exists
    if not Path(output_file).exists():
        print(f"⚠️  Output file not found: {output_file}")
        return
        
    try:
        import json
        
        with open(output_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        metadata = data.get('metadata', {})
        qas = data.get('qas', [])
        
        print(f"\n📊 Results Summary:")
        print(f"   • Total Q&A pairs: {len(qas)}")
        print(f"   • Generated at: {metadata.get('generated_at', 'Unknown')}")
        print(f"   • Model used: {metadata.get('model_used', 'Unknown')}")
        print(f"   • Playlist: {metadata.get('playlist_url', 'Unknown')}")
        
        if qas:
            print(f"\n📝 Sample Q&A:")
            sample_qa = qas[0]
            lines = sample_qa.split('\n')
            for line in lines[:4]:  # Show first few lines
                print(f"   {line}")
            if len(lines) > 4:
                print("   ...")
                
    except Exception as e:
        print(f"❌ Could not read results file: {e}")

def main():
    """Main entry point for the agent"""
    
    print("🤖 Automated YouTube Q&A Generation Agent")
    print("📺 Transform YouTube playlists into comprehensive Q&A datasets")
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Get playlist URL
    playlist_url = get_playlist_url()
    
    # Confirm before processing
    print(f"\n🔍 About to process: {playlist_url}")
    confirm = input("Continue? (y/N): ").strip().lower()
    
    if confirm not in ['y', 'yes']:
        print("Operation cancelled.")
        sys.exit(0)
    
    # Run the agent
    print("\n⏳ Starting agent processing...")
    print("   This may take several minutes depending on playlist size...")
    
    try:
        output_file = run_agent_sync(playlist_url)
        show_results_summary(output_file)
        
        if output_file:
            print(f"\n✨ All done! Check your results in: {output_file}")
        else:
            print("\n❌ Processing failed. Please check the errors above.")
            
    except KeyboardInterrupt:
        print("\n\n⏹️  Operation cancelled by user.")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

if __name__ == "__main__":
    main() 