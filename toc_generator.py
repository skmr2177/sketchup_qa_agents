#!/usr/bin/env python3
"""
Table of Contents (TOC) Generator for YouTube Playlists

This script automates the generation of a table of contents for YouTube playlists.
It extracts playlist information, checks for existing transcripts and Q&A files,
and generates a comprehensive CSV report with status information.

Usage:
    python toc_generator.py <playlist_url>
    python toc_generator.py --file playlist_urls.txt
"""

import os
import sys
import csv
import re
import json
import argparse
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from urllib.parse import urlparse, parse_qs
import subprocess
from datetime import datetime

# Try to import tabulate for nice terminal output
try:
    from tabulate import tabulate
    TABULATE_AVAILABLE = True
except ImportError:
    TABULATE_AVAILABLE = False
    print("⚠️  tabulate not available. Install with: pip install tabulate")
    print("   Will use basic table formatting instead.")

# Try to import pandas for alternative table formatting
try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    print("⚠️  pandas not available. Install with: pip install pandas")

# Try to import yt-dlp for playlist extraction
try:
    import yt_dlp
    YT_DLP_AVAILABLE = True
except ImportError:
    YT_DLP_AVAILABLE = False
    print("⚠️  yt-dlp not available. Install with: pip install yt-dlp")
    print("   Will use basic URL parsing instead.")


class TOCGenerator:
    """Generate Table of Contents for YouTube playlists"""
    
    def __init__(self, transcript_dir: str = "transcripts", output_dir: str = "output"):
        self.transcript_dir = Path(transcript_dir)
        self.output_dir = Path(output_dir)
        self.toc_file = Path("toc.csv")
        
        # Ensure directories exist
        self.transcript_dir.mkdir(exist_ok=True)
        self.output_dir.mkdir(exist_ok=True)
    
    def extract_playlist_id_from_url(self, url: str) -> Optional[str]:
        """Extract playlist ID from YouTube URL"""
        try:
            # Pattern to match playlist ID in various URL formats
            patterns = [
                r'list=([A-Za-z0-9_-]+)',  # Standard playlist parameter
                r'playlist\?list=([A-Za-z0-9_-]+)',  # Full playlist URL
                r'PL[A-Za-z0-9_-]+'  # Direct playlist ID
            ]
            
            for pattern in patterns:
                match = re.search(pattern, url)
                if match:
                    return match.group(1) if 'list=' in pattern else match.group(0)
            
            return None
        except Exception as e:
            print(f"❌ Error extracting playlist ID: {e}")
            return None
    
    def extract_video_id_from_url(self, url: str) -> Optional[str]:
        """Extract video ID from YouTube URL"""
        try:
            # Pattern to match video ID in various URL formats
            patterns = [
                r'v=([A-Za-z0-9_-]+)',  # Standard video parameter
                r'youtu\.be/([A-Za-z0-9_-]+)',  # Short URL format
                r'youtube\.com/watch\?.*v=([A-Za-z0-9_-]+)',  # Full URL format
            ]
            
            for pattern in patterns:
                match = re.search(pattern, url)
                if match:
                    return match.group(1)
            
            return None
        except Exception as e:
            print(f"❌ Error extracting video ID: {e}")
            return None
    
    def is_playlist_url(self, url: str) -> bool:
        """Check if URL is a playlist URL"""
        return 'list=' in url or url.startswith('PL')
    
    def is_video_url(self, url: str) -> bool:
        """Check if URL is a video URL"""
        return 'v=' in url or 'youtu.be/' in url
    
    def get_clean_playlist_url(self, url: str) -> str:
        """Convert any playlist URL to clean playlist URL format"""
        playlist_id = self.extract_playlist_id_from_url(url)
        if playlist_id:
            return f"https://www.youtube.com/playlist?list={playlist_id}"
        return url
    
    def get_playlist_info_with_yt_dlp(self, playlist_url: str) -> Tuple[Optional[str], Optional[str], List[Dict]]:
        """Get playlist title and video list using yt-dlp"""
        if not YT_DLP_AVAILABLE:
            return None, None, []
        
        try:
            ydl_opts = {
                'quiet': False,  # Show progress for debugging
                'no_warnings': False,  # Show warnings
                'extract_flat': True,
                'ignoreerrors': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                playlist_info = ydl.extract_info(playlist_url, download=False)
                
                if not playlist_info:
                    print(f"❌ No playlist info returned from yt-dlp")
                    return None, None, []
                
                playlist_title = playlist_info.get('title', 'Unknown Playlist')
                
                # Always get full playlist info from YouTube
                videos = []
                if 'entries' in playlist_info:
                    for entry in playlist_info['entries']:
                        if entry and entry.get('id'):
                            videos.append({
                                'id': entry['id'],
                                'title': entry.get('title', f"Video {entry['id']}"),
                                'url': entry.get('url', f"https://www.youtube.com/watch?v={entry['id']}"),
                                'duration': entry.get('duration'),
                                'uploader': entry.get('uploader'),
                            })
                
                print(f"✅ Successfully extracted {len(videos)} videos from YouTube")
                return playlist_title, playlist_url, videos
                
        except Exception as e:
            print(f"❌ Error getting playlist info with yt-dlp: {e}")
            return None, None, []
    
    def get_playlist_info_basic(self, playlist_url: str) -> Tuple[Optional[str], Optional[str], List[Dict]]:
        """Basic playlist info extraction without yt-dlp"""
        playlist_id = self.extract_playlist_id_from_url(playlist_url)
        if not playlist_id:
            return None, None, []
        
        # Try to get videos from existing transcript files
        videos = self.get_videos_from_transcripts(playlist_id)
        playlist_title = f"Playlist {playlist_id}"
        
        return playlist_title, playlist_url, videos
    
    def get_videos_from_transcripts(self, playlist_id: str) -> List[Dict]:
        """Extract video information from existing transcript files"""
        videos = []
        playlist_folder = self.transcript_dir / playlist_id
        
        if not playlist_folder.exists():
            return videos
        
        for transcript_file in playlist_folder.glob("*.txt"):
            if transcript_file.name.startswith("temp_"):
                continue
            
            # Extract video info from filename
            video_info = self.extract_video_info_from_filename(transcript_file.name)
            if video_info:
                videos.append(video_info)
        
        # Sort by playlist index if available
        videos.sort(key=lambda x: int(x.get('playlist_index', 0)))
        return videos
    
    def extract_video_info_from_filename(self, filename: str) -> Optional[Dict]:
        """Extract video ID and title from transcript filename"""
        # Pattern: playlist_XX_video_VIDEOID_Title.txt
        pattern = r'playlist_(\d+)_video_([A-Za-z0-9_-]+)_(.+)\.txt'
        match = re.search(pattern, filename)
        
        if match:
            playlist_index = match.group(1)
            video_id = match.group(2)
            title = match.group(3).replace('_', ' ')
            return {
                'id': video_id,
                'title': title,
                'playlist_index': playlist_index,
                'url': f"https://www.youtube.com/watch?v={video_id}"
            }
        
        # Fallback pattern: video_VIDEOID_Title.txt
        pattern2 = r'video_([A-Za-z0-9_-]+)_(.+)\.txt'
        match2 = re.search(pattern2, filename)
        
        if match2:
            video_id = match2.group(1)
            title = match2.group(2).replace('_', ' ')
            return {
                'id': video_id,
                'title': title,
                'playlist_index': '0',
                'url': f"https://www.youtube.com/watch?v={video_id}"
            }
        
        return None
    
    def check_transcript_exists(self, playlist_id: str, video_id: str, video_title: str) -> Tuple[bool, str]:
        """Check if transcript file exists for a video"""
        playlist_folder = self.transcript_dir / playlist_id
        
        if not playlist_folder.exists():
            return False, "Playlist folder not found"
        
        # Look for transcript file
        for transcript_file in playlist_folder.glob("*.txt"):
            if transcript_file.name.startswith("temp_"):
                continue
            
            if video_id in transcript_file.name:
                # Return the relative path to the transcript file
                relative_path = transcript_file.relative_to(self.transcript_dir.parent)
                return True, f"📄 {relative_path}"
        
        return False, "❌"
    
    def check_qa_exists(self, playlist_id: str, video_id: str, video_title: str) -> Tuple[bool, str]:
        """Check if Q&A file exists for a video"""
        playlist_output_folder = self.output_dir / playlist_id
        
        if not playlist_output_folder.exists():
            return False, "❌"
        
        # Look for Q&A files with the pattern: video_<video_id>_<title>_QnA.md
        for qa_file in playlist_output_folder.glob("*.md"):
            if qa_file.name.startswith(f"video_{video_id}_") and qa_file.name.endswith("_QnA.md"):
                # Return the relative path to the Q&A file
                relative_path = qa_file.relative_to(self.output_dir.parent)
                return True, f"📋 {relative_path}"
        
        # Also check for any file containing the video ID and QnA in the name
        for qa_file in playlist_output_folder.glob("*"):
            if video_id in qa_file.name and "QnA" in qa_file.name:
                # Return the relative path to the Q&A file
                relative_path = qa_file.relative_to(self.output_dir.parent)
                return True, f"📋 {relative_path}"
        
        return False, "❌"
    
    def generate_toc_for_single_video(self, video_url: str) -> List[Dict]:
        """Generate TOC data for a single video"""
        print(f"🎬 Processing single video: {video_url}")
        
        # Extract video ID
        video_id = self.extract_video_id_from_url(video_url)
        if not video_id:
            print(f"❌ Could not extract video ID from URL")
            return []
        
        print(f"📺 Video ID: {video_id}")
        
        # Try to get video info from yt-dlp
        video_title = f"Video {video_id}"
        if YT_DLP_AVAILABLE:
            try:
                ydl_opts = {
                    'quiet': True,
                    'no_warnings': True,
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    video_info = ydl.extract_info(video_url, download=False)
                    if video_info:
                        video_title = video_info.get('title', video_title)
                        print(f"📝 Video Title: {video_title}")
            except Exception as e:
                print(f"⚠️  Could not get video info from YouTube: {e}")
        
        # Check if this video exists in any playlist
        video_data = self.find_video_in_playlists(video_id, video_title)
        
        if not video_data:
            # Create a standalone video entry
            video_data = [{
                'id': video_id,
                'title': video_title,
                'url': video_url,
                'playlist_id': 'standalone',
                'playlist_title': 'Standalone Video',
                'playlist_index': '0'
            }]
        
        # Convert video data to TOC entries
        toc_data = []
        for video in video_data:
            playlist_id = video['playlist_id']
            
            # Check for transcript
            transcript_exists, transcript_status = self.check_transcript_exists(
                playlist_id, video['id'], video['title']
            )
            
            # Check for Q&A
            qa_exists, qa_status = self.check_qa_exists(
                playlist_id, video['id'], video['title']
            )
            
            # Generate error message if needed
            error_msg = ""
            if not transcript_exists:
                error_msg += "Missing transcript; "
            if not qa_exists:
                error_msg += "Missing Q&A; "
            error_msg = error_msg.rstrip("; ")
            
            toc_entry = {
                'playlist_id': playlist_id,
                'playlist_title': video['playlist_title'],
                'video_title': video['title'],
                'video_id': video['id'],
                'video_url': video['url'],
                'transcript': transcript_status,
                'qa': qa_status,
                'error_message': error_msg,
                'playlist_index': video.get('playlist_index', '0'),
                'processed_at': datetime.now().isoformat()
            }
            
            toc_data.append(toc_entry)
        
        return toc_data
    
    def find_video_in_playlists(self, video_id: str, video_title: str) -> List[Dict]:
        """Find a video in existing playlist transcripts"""
        videos = []
        
        # Search through all playlist directories
        for playlist_folder in self.transcript_dir.iterdir():
            if not playlist_folder.is_dir():
                continue
            
            playlist_id = playlist_folder.name
            if playlist_id.startswith('temp_'):
                continue
            
            # Check if this video exists in this playlist
            for transcript_file in playlist_folder.glob("*.txt"):
                if transcript_file.name.startswith("temp_"):
                    continue
                
                if video_id in transcript_file.name:
                    # Extract playlist info
                    video_info = self.extract_video_info_from_filename(transcript_file.name)
                    if video_info:
                        video_info['playlist_id'] = playlist_id
                        video_info['playlist_title'] = f"Playlist {playlist_id}"
                        videos.append(video_info)
                        break
        
        return videos
    
    def generate_toc_for_playlist(self, playlist_url: str) -> List[Dict]:
        """Generate TOC data for a single playlist"""
        print(f"🎯 Processing playlist: {playlist_url}")
        
        # Extract playlist ID and get clean playlist URL
        playlist_id = self.extract_playlist_id_from_url(playlist_url)
        if not playlist_id:
            print(f"❌ Could not extract playlist ID from URL")
            return []
        
        clean_playlist_url = self.get_clean_playlist_url(playlist_url)
        print(f"📁 Playlist ID: {playlist_id}")
        print(f"🔗 Clean URL: {clean_playlist_url}")
        
        # Get playlist information
        videos = []
        playlist_title = None
        
        # Always try to get full playlist from YouTube first
        if YT_DLP_AVAILABLE:
            playlist_title, _, videos = self.get_playlist_info_with_yt_dlp(clean_playlist_url)
            if videos:
                print(f"📺 Successfully got {len(videos)} videos from YouTube")
            else:
                print(f"⚠️  yt-dlp failed to get full playlist")
        
        # Only fall back to existing transcripts if yt-dlp completely failed
        if not videos:
            print(f"⚠️  Falling back to existing transcripts...")
            playlist_title, _, videos = self.get_playlist_info_basic(playlist_url)
            if videos:
                print(f"📺 Found {len(videos)} videos from existing transcripts")
        
        if not videos:
            print(f"❌ No videos found for playlist {playlist_id}")
            return []
        
        print(f"📺 Processing {len(videos)} videos")
        
        # Generate TOC data for each video
        toc_data = []
        for video in videos:
            video_id = video['id']
            video_title = video['title']
            
            # Check for transcript
            transcript_exists, transcript_status = self.check_transcript_exists(
                playlist_id, video_id, video_title
            )
            
            # Check for Q&A
            qa_exists, qa_status = self.check_qa_exists(
                playlist_id, video_id, video_title
            )
            
            # Generate error message if needed
            error_msg = ""
            if not transcript_exists:
                error_msg += "Missing transcript; "
            if not qa_exists:
                error_msg += "Missing Q&A; "
            error_msg = error_msg.rstrip("; ")
            
            toc_entry = {
                'playlist_id': playlist_id,
                'playlist_title': playlist_title or f"Playlist {playlist_id}",
                'video_title': video_title,
                'video_id': video_id,
                'video_url': video['url'],
                'transcript': transcript_status,
                'qa': qa_status,
                'error_message': error_msg,
                'playlist_index': video.get('playlist_index', '0'),
                'processed_at': datetime.now().isoformat()
            }
            
            toc_data.append(toc_entry)
        
        return toc_data
    
    def update_toc_csv(self, new_data: List[Dict], append: bool = True):
        """Update the TOC CSV file with new data"""
        if not new_data:
            return
        
        # Define CSV headers
        headers = [
            'playlist_id', 'playlist_title', 'video_title', 'video_id', 
            'video_url', 'transcript', 'qa', 'error_message', 
            'playlist_index', 'processed_at'
        ]
        
        # Read existing data if appending
        existing_data = []
        if append and self.toc_file.exists():
            try:
                with open(self.toc_file, 'r', newline='', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    existing_data = list(reader)
            except Exception as e:
                print(f"⚠️  Error reading existing TOC file: {e}")
        
        # Combine data (remove duplicates based on playlist_id + video_id)
        combined_data = existing_data.copy()
        existing_keys = {(row['playlist_id'], row['video_id']) for row in existing_data}
        
        for entry in new_data:
            key = (entry['playlist_id'], entry['video_id'])
            if key not in existing_keys:
                combined_data.append(entry)
                existing_keys.add(key)
        
        # Write to CSV
        try:
            with open(self.toc_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writeheader()
                writer.writerows(combined_data)
            
            print(f"📄 TOC updated: {self.toc_file}")
            print(f"   Total entries: {len(combined_data)}")
            
        except Exception as e:
            print(f"❌ Error writing TOC file: {e}")
    
    def display_toc_table(self, data: List[Dict]):
        """Display TOC data as a formatted table"""
        if not data:
            print("❌ No data to display")
            return
        
        # Prepare table data
        table_data = []
        for entry in data:
            # Create compact display for file paths
            transcript_display = entry['transcript']
            if transcript_display.startswith('📄'):
                # Extract just the filename for display
                path_parts = transcript_display.split('\\')
                if len(path_parts) > 2:
                    transcript_display = f"📄 {path_parts[-1]}"
            elif transcript_display == "❌":
                transcript_display = "❌ Not available"
            
            qa_display = entry['qa']
            if qa_display.startswith('📋'):
                # Extract just the filename for display
                path_parts = qa_display.split('\\')
                if len(path_parts) > 2:
                    qa_display = f"📋 {path_parts[-1]}"
            elif qa_display == "❌":
                qa_display = "❌ Not available"
            
            table_data.append([
                entry['playlist_id'][:15] + "..." if len(entry['playlist_id']) > 15 else entry['playlist_id'],
                entry['video_title'][:35] + "..." if len(entry['video_title']) > 35 else entry['video_title'],
                transcript_display,
                qa_display,
                entry['error_message'][:20] + "..." if len(entry['error_message']) > 20 else entry['error_message']
            ])
        
        headers = ['Playlist ID', 'Video Title', 'Transcript', 'Q&A', 'Errors']
        
        # Display table
        if TABULATE_AVAILABLE:
            print("\n" + "="*100)
            print("📋 TABLE OF CONTENTS")
            print("="*100)
            print(tabulate(table_data, headers=headers, tablefmt='grid'))
        elif PANDAS_AVAILABLE:
            df = pd.DataFrame(table_data, columns=headers)
            print("\n" + "="*100)
            print("📋 TABLE OF CONTENTS")
            print("="*100)
            print(df.to_string(index=False))
        else:
            # Basic table formatting
            print("\n" + "="*100)
            print("📋 TABLE OF CONTENTS")
            print("="*100)
            print(f"{'Playlist ID':<20} {'Video Title':<40} {'Transcript':<10} {'Q&A':<5} {'Errors':<30}")
            print("-" * 100)
            for row in table_data:
                print(f"{row[0]:<20} {row[1]:<40} {row[2]:<10} {row[3]:<5} {row[4]:<30}")
        
        # Summary statistics
        total_videos = len(data)
        transcripts_available = sum(1 for entry in data if entry['transcript'].startswith('📄'))
        qa_available = sum(1 for entry in data if entry['qa'].startswith('📋'))
        
        print(f"\n📊 SUMMARY:")
        print(f"   Total Videos: {total_videos}")
        print(f"   Transcripts Available: {transcripts_available}/{total_videos} ({transcripts_available/total_videos*100:.1f}%)")
        print(f"   Q&A Available: {qa_available}/{total_videos} ({qa_available/total_videos*100:.1f}%)")
    
    def process_urls(self, urls: List[str], append: bool = True):
        """Process multiple URLs (can be video or playlist URLs)"""
        all_toc_data = []
        
        for i, url in enumerate(urls, 1):
            print(f"\n🎬 Processing URL {i}/{len(urls)}")
            print("-" * 50)
            
            if self.is_playlist_url(url):
                print(f"📋 Detected playlist URL")
                toc_data = self.generate_toc_for_playlist(url)
            elif self.is_video_url(url):
                print(f"🎬 Detected video URL")
                toc_data = self.generate_toc_for_single_video(url)
            else:
                print(f"❌ Unknown URL format: {url}")
                continue
            
            all_toc_data.extend(toc_data)
        
        # Update CSV file
        if all_toc_data:
            self.update_toc_csv(all_toc_data, append=append)
            self.display_toc_table(all_toc_data)
        else:
            print("❌ No TOC data generated")
    
    def process_playlist_urls(self, playlist_urls: List[str], append: bool = True):
        """Process multiple playlist URLs (legacy method)"""
        self.process_urls(playlist_urls, append)


def read_playlist_urls_from_file(filename: str) -> List[str]:
    """Read playlist URLs from a text file"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f if line.strip() and 
                   ('youtube.com' in line or 'youtu.be' in line)]
        return urls
    except Exception as e:
        print(f"❌ Error reading playlist URLs from {filename}: {e}")
        return []


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Generate Table of Contents for YouTube playlists",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python toc_generator.py "https://www.youtube.com/playlist?list=PL-xxxxx"
  python toc_generator.py "https://www.youtube.com/watch?v=xxxxx"
  python toc_generator.py --file urls.txt
  python toc_generator.py --no-append "https://www.youtube.com/watch?v=xxxxx"
        """
    )
    
    parser.add_argument(
        'url',
        nargs='?',
        help='YouTube video or playlist URL'
    )
    
    parser.add_argument(
        '--file', '-f',
        help='File containing YouTube URLs (video or playlist, one per line)'
    )
    
    parser.add_argument(
        '--no-append',
        action='store_true',
        help='Replace existing TOC instead of appending'
    )
    
    parser.add_argument(
        '--transcript-dir',
        default='transcripts',
        help='Directory containing transcript files (default: transcripts)'
    )
    
    parser.add_argument(
        '--output-dir',
        default='output',
        help='Directory containing Q&A files (default: output)'
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if not args.url and not args.file:
        # Interactive mode - ask for URL
        print("\n🎯 Interactive TOC Generator")
        print("=" * 50)
        print("Enter a YouTube video or playlist URL to generate TOC")
        print("Examples:")
        print("  - https://www.youtube.com/watch?v=xxxxx")
        print("  - https://www.youtube.com/playlist?list=PL-xxxxx")
        print("  - https://youtu.be/xxxxx")
        print()
        
        while True:
            url = input("📥 Enter YouTube URL: ").strip()
            if not url:
                print("❌ Please enter a valid URL")
                continue
                
            if "youtube.com" not in url and "youtu.be" not in url:
                print("❌ Please enter a valid YouTube URL")
                continue
                
            break
        
        args.url = url
    
    # Initialize TOC generator
    toc_gen = TOCGenerator(
        transcript_dir=args.transcript_dir,
        output_dir=args.output_dir
    )
    
    # Get URLs
    urls = []
    
    if args.file:
        urls = read_playlist_urls_from_file(args.file)
        if not urls:
            print(f"❌ No valid YouTube URLs found in {args.file}")
            sys.exit(1)
    else:
        urls = [args.url]
    
    # Process URLs
    try:
        toc_gen.process_urls(urls, append=not args.no_append)
        print(f"\n✅ TOC generation completed successfully!")
        
    except KeyboardInterrupt:
        print(f"\n⚠️  TOC generation interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error during TOC generation: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 