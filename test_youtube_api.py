#!/usr/bin/env python3
"""
Test script to check if YouTube Transcript API is working
"""

import sys
try:
    from youtube_transcript_api import YouTubeTranscriptApi
    print("✅ YouTube Transcript API imported successfully")
except ImportError as e:
    print(f"❌ Failed to import YouTube Transcript API: {e}")
    sys.exit(1)

def test_api():
    """Test the YouTube Transcript API with a simple video"""
    print("🧪 Testing YouTube Transcript API...")
    
    # Test with a simple, well-known video that should have transcripts
    test_video_id = "dQw4w9WgXcQ"  # Rick Astley - Never Gonna Give You Up
    
    print(f"📋 Testing with video ID: {test_video_id}")
    
    try:
        print("🔍 Attempting to get transcript...")
        transcript_list = YouTubeTranscriptApi.get_transcript(test_video_id, languages=['en'])
        
        if transcript_list:
            print(f"✅ Success! Found {len(transcript_list)} transcript entries")
            print(f"📝 First few words: {transcript_list[0]['text'][:50]}...")
            return True
        else:
            print("❌ No transcript found")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_api()
    if success:
        print("✅ YouTube Transcript API is working!")
    else:
        print("❌ YouTube Transcript API is not working!")
    sys.exit(0 if success else 1) 