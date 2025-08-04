#!/usr/bin/env python3
"""
Interactive Table of Contents (TOC) Generator for YouTube

This script provides an interactive interface to generate TOC for YouTube videos or playlists.
Simply run the script and it will ask for your input URL.
"""

import sys
import os
from toc_generator import TOCGenerator

def get_user_input():
    """Get URL input from user"""
    print("🎯 Interactive TOC Generator for YouTube")
    print("=" * 50)
    print()
    print("Enter a YouTube URL (video or playlist):")
    print("Examples:")
    print("  • Video: https://www.youtube.com/watch?v=xxxxx")
    print("  • Playlist: https://www.youtube.com/playlist?list=PL-xxxxx")
    print("  • Short URL: https://youtu.be/xxxxx")
    print()
    
    while True:
        url = input("📥 Enter YouTube URL: ").strip()
        
        if not url:
            print("❌ Please enter a valid URL")
            continue
            
        if "youtube.com" not in url and "youtu.be" not in url:
            print("❌ Please enter a valid YouTube URL")
            continue
            
        return url

def main():
    """Main interactive function"""
    try:
        # Get URL from user
        url = get_user_input()
        
        print(f"\n🎬 Processing: {url}")
        print("-" * 50)
        
        # Initialize TOC generator
        toc_gen = TOCGenerator()
        
        # Process the URL
        toc_gen.process_urls([url], append=False)
        
        print(f"\n✅ TOC generation completed successfully!")
        print(f"📄 Results saved to: toc.csv")
        
        # Ask if user wants to continue
        while True:
            choice = input("\n🔄 Generate TOC for another URL? (y/n): ").strip().lower()
            if choice in ['y', 'yes']:
                print("\n" + "="*50)
                main()  # Restart
                break
            elif choice in ['n', 'no']:
                print("👋 Goodbye!")
                break
            else:
                print("❌ Please enter 'y' or 'n'")
        
    except KeyboardInterrupt:
        print(f"\n⚠️  TOC generation interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error during TOC generation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 