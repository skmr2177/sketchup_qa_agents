#!/usr/bin/env python3
"""
YouTube Transcript Downloader using YouTube Transcript API
=========================================================

Download transcripts from multiple YouTube playlists using the YouTube Transcript API.
This is specifically designed for caption extraction and has much higher success rates.

Features:
- Uses YouTube Transcript API (specifically designed for captions)
- Processes multiple playlists from config file
- Handles both manual and auto-generated captions
- Progress tracking with tqdm
- Error handling and retry logic
- Rate limiting to avoid API limits
- Clean transcript formatting

Usage:
    python download_transcripts_api.py

Requirements:
    - youtube-transcript-api installed (pip install youtube-transcript-api)
    - skecthup_playlist.txt file with playlist URLs (one per line)
"""

import os
import sys
import time
import re
import json
from datetime import datetime
from typing import List, Dict, Optional

try:
    from youtube_transcript_api import YouTubeTranscriptApi
    from tqdm import tqdm
    from colorama import init, Fore, Style
except ImportError as e:
    print(f"❌ Missing required package: {e}")
    print("📦 Please install: pip install youtube-transcript-api tqdm colorama")
    sys.exit(1)

# Initialize colorama
init(autoreset=True)

class YouTubeTranscriptDownloader:
    """Download transcripts from multiple YouTube playlists using YouTube Transcript API"""

    def __init__(self, transcript_dir: str = "transcripts"):
        self.transcript_dir = transcript_dir
        self.total_success_count = 0
        self.total_failed_videos = []
        self.total_skipped_videos = []
        self.playlist_results = []
        os.makedirs(self.transcript_dir, exist_ok=True)
        print(f"{Fore.GREEN}📁 Using transcripts folder: '{transcript_dir}'{Style.RESET_ALL}")

    def read_playlist_urls(self, filename: str = "skecthup_playlist.txt") -> List[str]:
        """Read all playlist URLs from file"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                urls = [line.strip() for line in f.readlines() if line.strip() and ('youtube.com' in line or 'youtu.be' in line)]
                if not urls:
                    print(f"❌ No valid YouTube URLs found in {filename}")
                    return []
                print(f"{Fore.GREEN}✅ Found {len(urls)} playlist URLs in {filename}{Style.RESET_ALL}")
                return urls
        except FileNotFoundError:
            print(f"❌ File {filename} not found")
            return []
        except Exception as e:
            print(f"❌ Error reading {filename}: {e}")
            return []

    def get_video_info(self, video_id: str) -> Optional[Dict]:
        """Get basic video information using yt-dlp"""
        try:
            import subprocess
            import json as json_module
            
            command = [
                sys.executable, "-m", "yt_dlp",
                "--dump-json",
                "--no-playlist",
                f"https://www.youtube.com/watch?v={video_id}"
            ]
            
            result = subprocess.run(command, capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                data = json_module.loads(result.stdout)
                return {
                    'id': video_id,
                    'title': data.get('title', f'Video {video_id}'),
                    'duration': data.get('duration', 0),
                    'uploader': data.get('uploader', 'Unknown')
                }
        except Exception as e:
            print(f"   ⚠️  Could not get video info for {video_id}: {e}")
        
        # Fallback to basic info
        return {
            'id': video_id,
            'title': f'Video {video_id}',
            'duration': 0,
            'uploader': 'Unknown'
        }

    def download_video_transcript(self, video_id: str, playlist_index: int, playlist_url: str) -> bool:
        """Download transcript for a single video using YouTube Transcript API"""
        try:
            # Get video info
            video_info = self.get_video_info(video_id)
            video_title = video_info['title']
            
            # Create filename
            safe_title = re.sub(r'[<>:"/\\|?*]', '_', video_title)
            filename = f"playlist_{playlist_index:02d}_video_{video_id}_{safe_title[:50]}.txt"
            
            # Check for existing file in multiple possible locations
            possible_paths = [
                # Check in root transcripts folder (old format)
                os.path.join(self.transcript_dir, filename),
                # Check in organized playlist folders
                os.path.join(self.transcript_dir, f"PL-bndkJaV8A4ofk43YYdTZaG4TJWqgOIa", f"video_{video_id}_{safe_title[:50]}.txt"),
                os.path.join(self.transcript_dir, f"PL-bndkJaV8A65rVfOEqQ7VYJc46cerIqf", f"video_{video_id}_{safe_title[:50]}.txt"),
                os.path.join(self.transcript_dir, f"PL-bndkJaV8A6lnfX-GTNSW64I_xa5ofQp", f"video_{video_id}_{safe_title[:50]}.txt"),
                os.path.join(self.transcript_dir, f"PL-bndkJaV8A7fQttkdQ2sTfLjZxI5UeS2", f"video_{video_id}_{safe_title[:50]}.txt"),
                os.path.join(self.transcript_dir, f"PL-bndkJaV8A438k9GoBVKA5Xy3OLk_1hn", f"video_{video_id}_{safe_title[:50]}.txt"),
                os.path.join(self.transcript_dir, f"PL-bndkJaV8A5VmrwvxMw-IYgSJLlV-vjH", f"video_{video_id}_{safe_title[:50]}.txt"),
                os.path.join(self.transcript_dir, f"PL-bndkJaV8A5lpn6Nn8ctOBbd0cVrHEE8", f"video_{video_id}_{safe_title[:50]}.txt"),
                os.path.join(self.transcript_dir, f"PL-bndkJaV8A5U5nTBIp9qWmGQrzcKNJSZ", f"video_{video_id}_{safe_title[:50]}.txt"),
                os.path.join(self.transcript_dir, f"PL-bndkJaV8A7R2t970OmHY6kPGJwTfGP2", f"video_{video_id}_{safe_title[:50]}.txt"),
                os.path.join(self.transcript_dir, f"PL-bndkJaV8A7FiNCukanBSpxK3lIFG2KK", f"video_{video_id}_{safe_title[:50]}.txt"),
            ]
            
            # Check if file already exists in any location
            existing_file = None
            for path in possible_paths:
                if os.path.exists(path):
                    existing_file = path
                    break
            
            if existing_file:
                if video_id not in self.total_skipped_videos:
                    self.total_skipped_videos.append(video_id)
                print(f"   ⏭️  Skipping {video_id} - already exists: {os.path.basename(existing_file)}")
                return True

            print(f"   🔍 Video {video_id} not found - downloading transcript...")

            # Get transcript using YouTube Transcript API with multiple strategies
            transcript_list = None
            max_retries = 3
            retry_count = 0
            
            # Different language combinations to try
            language_combinations = [
                ['en', 'en-US', 'en-GB'],
                ['en'],
                ['en-US'],
                ['en-GB'],
                ['auto'],  # Auto-generated captions
                ['en', 'auto'],
                ['auto', 'en']
            ]
            
            while retry_count < max_retries and transcript_list is None:
                for lang_combo in language_combinations:
                    try:
                        print(f"   🔄 Attempt {retry_count + 1}: Trying languages {lang_combo}")
                        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=lang_combo)
                        if transcript_list:
                            print(f"   ✅ Success with languages: {lang_combo}")
                            break
                    except Exception as e:
                        error_msg = str(e)
                        print(f"   ❌ REAL ERROR with languages {lang_combo}: {error_msg}")
                        if "IP" in error_msg or "blocked" in error_msg.lower():
                            print(f"   🚫 IP blocked - waiting longer...")
                            time.sleep(30)  # Wait 30 seconds for IP blocking
                        elif "No transcript found" in error_msg:
                            print(f"   ⚠️  No transcript found with languages: {lang_combo}")
                            continue
                        else:
                            print(f"   ⚠️  Continuing to next language combination...")
                            continue
                
                if transcript_list:
                    break
                    
                retry_count += 1
                if retry_count < max_retries:
                    wait_time = 60 * retry_count  # Progressive waiting: 60s, 120s, 180s
                    print(f"   ⏳ All language combinations failed. Waiting {wait_time} seconds before retry {retry_count + 1}...")
                    time.sleep(wait_time)
                else:
                    print(f"   ❌ All {max_retries} attempts failed for {video_id}")
            
            if not transcript_list:
                self.total_failed_videos.append({
                    'id': video_id, 
                    'title': video_title, 
                    'playlist_index': playlist_index, 
                    'reason': 'No transcript found after all attempts'
                })
                return False

            # Extract text from transcript
            transcript_text = ""
            for entry in transcript_list:
                transcript_text += entry['text'] + " "

            # Clean up the text
            transcript_text = re.sub(r'\s+', ' ', transcript_text).strip()

            if len(transcript_text) > 50:
                # Save transcript in root folder (will be organized later)
                filepath = os.path.join(self.transcript_dir, filename)
                try:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(f"Title: {video_title}\n")
                        f.write(f"Video ID: {video_id}\n")
                        f.write(f"Playlist Index: {playlist_index}\n")
                        f.write(f"Playlist URL: {playlist_url}\n")
                        f.write(f"Video URL: https://www.youtube.com/watch?v={video_id}\n")
                        f.write(f"Uploader: {video_info['uploader']}\n")
                        f.write(f"Duration: {video_info['duration']} seconds\n")
                        f.write(f"Downloaded: {datetime.now().isoformat()}\n")
                        f.write("-" * 80 + "\n\n")
                        f.write(transcript_text)
                    
                    # Verify file was actually created
                    if os.path.exists(filepath) and os.path.getsize(filepath) > 100:
                        print(f"   ✅ Successfully downloaded and saved: {video_title[:40]}...")
                        print(f"   📁 Saved to: {os.path.basename(filepath)}")
                        return True
                    else:
                        print(f"   ❌ File creation failed for {video_id}")
                        return False
                        
                except Exception as e:
                    print(f"   ❌ Error saving file for {video_id}: {str(e)}")
                    return False
            else:
                print(f"   ❌ Transcript too short ({len(transcript_text)} chars) for {video_id}")
                self.total_failed_videos.append({
                    'id': video_id, 
                    'title': video_title, 
                    'playlist_index': playlist_index, 
                    'reason': 'Transcript too short or empty'
                })
                return False

        except Exception as e:
            error_msg = str(e)
            print(f"   💥 FINAL ERROR for video {video_id}: {error_msg}")
            if "IP" in error_msg or "blocked" in error_msg.lower():
                reason = "IP blocked by YouTube"
            elif "No transcript found" in error_msg:
                reason = "No transcript available"
            elif "Video unavailable" in error_msg:
                reason = "Video unavailable"
            elif "Private video" in error_msg:
                reason = "Private video"
            else:
                reason = f"API error: {error_msg}"
            
            self.total_failed_videos.append({
                'id': video_id, 
                'title': f'Video {video_id}', 
                'playlist_index': playlist_index, 
                'reason': reason
            })
            return False



    def extract_playlist_videos(self, playlist_url: str, playlist_index: int) -> List[str]:
        """Extract video IDs from playlist using yt-dlp"""
        print(f"{Fore.CYAN}🔍 [{playlist_index}] Extracting video information...{Style.RESET_ALL}")
        
        try:
            import subprocess
            import json as json_module
            
            command = [
                sys.executable, "-m", "yt_dlp",
                "--flat-playlist",
                "--dump-json",
                playlist_url
            ]
            
            result = subprocess.run(command, capture_output=True, text=True, timeout=60)
            if result.returncode != 0:
                print(f"{Fore.RED}   ❌ Failed to get video list: {result.stderr}{Style.RESET_ALL}")
                return []
            
            videos = []
            for line in result.stdout.strip().split('\n'):
                try:
                    entry = json_module.loads(line)
                    if entry and entry.get('id'):
                        videos.append(entry['id'])
                except json_module.JSONDecodeError:
                    continue
                    
            print(f"{Fore.GREEN}   ✅ Found {len(videos)} videos in playlist{Style.RESET_ALL}")
            return videos
            
        except Exception as e:
            print(f"{Fore.RED}   ❌ Error extracting videos: {e}{Style.RESET_ALL}")
            return []

    def process_video_batch(self, video_ids: List[str], playlist_index: int, playlist_url: str, delay_between_videos: int = 3) -> tuple:
        """Process a batch of videos one by one with detailed progress tracking"""
        success_count = 0
        failed_count = 0
        skipped_count = 0
        
        print(f"{Fore.CYAN}📋 Processing {len(video_ids)} videos one by one...{Style.RESET_ALL}")
        
        for i, video_id in enumerate(video_ids, 1):
            print(f"\n{Fore.CYAN}[{playlist_index}.{i:03d}/{len(video_ids)}] Processing video {video_id}...{Style.RESET_ALL}")
            
            try:
                # Process the video
                result = self.download_video_transcript(video_id, playlist_index, playlist_url)
                
                if result:
                    success_count += 1
                    print(f"   ✅ Success ({success_count}/{len(video_ids)})")
                else:
                    failed_count += 1
                    print(f"   ❌ Failed ({failed_count}/{len(video_ids)})")
                    
            except Exception as e:
                failed_count += 1
                print(f"   💥 PROCESSING ERROR for {video_id}: {str(e)}")
                self.total_failed_videos.append({
                    'id': video_id, 
                    'title': f'Video {video_id}', 
                    'playlist_index': playlist_index, 
                    'reason': f'Processing error: {str(e)}'
                })
            
            # Add delay between videos (except for the last one)
            if delay_between_videos > 0 and i < len(video_ids):
                print(f"   ⏳ Waiting {delay_between_videos} seconds...")
                time.sleep(delay_between_videos)
        
        # Count skipped videos
        skipped_count = len([vid for vid in video_ids if vid in self.total_skipped_videos])
        
        return success_count, failed_count, skipped_count

    def download_all_playlists(self, delay_between_videos: int = 3, start_from_playlist: int = 5) -> int:
        """Download transcripts from all playlists"""
        print(f"{Fore.YELLOW}🎬 Starting transcript download with YouTube Transcript API...{Style.RESET_ALL}")
        
        playlist_urls = self.read_playlist_urls()
        if not playlist_urls:
            return 0
        
        # Filter playlists to start from specified playlist
        filtered_playlists = list(enumerate(playlist_urls, 1))[start_from_playlist-1:]
        print(f"{Fore.GREEN}📥 Processing {len(filtered_playlists)} playlists (starting from playlist {start_from_playlist})...{Style.RESET_ALL}")
        
        for playlist_index, playlist_url in filtered_playlists:
            print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
            print(f"🎬 PLAYLIST {playlist_index}/{len(playlist_urls)}: {playlist_url.split('list=')[1]}{Style.RESET_ALL}")
            print(f"{'='*60}{Style.RESET_ALL}")
            
            video_ids = self.extract_playlist_videos(playlist_url, playlist_index)
            if not video_ids:
                self.playlist_results.append({
                    'playlist_index': playlist_index, 
                    'playlist_url': playlist_url, 
                    'success': 0, 'failed': 0, 'skipped': 0, 'total': 0
                })
                continue
            
            # Process all videos one by one
            success, failed, skipped = self.process_video_batch(video_ids, playlist_index, playlist_url, delay_between_videos)
            
            self.total_success_count += success
            self.playlist_results.append({
                'playlist_index': playlist_index, 
                'playlist_url': playlist_url, 
                'success': success, 
                'failed': failed, 
                'skipped': skipped, 
                'total': len(video_ids)
            })
            
            print(f"\n{Fore.GREEN}📊 Playlist {playlist_index} Summary:{Style.RESET_ALL}")
            print(f"   ✅ Success: {success}")
            print(f"   ❌ Failed: {failed}")
            print(f"   ⏭️  Skipped: {skipped}")
            print(f"   📋 Total: {len(video_ids)}")
            
            if playlist_index < len(playlist_urls):
                wait_time = 30  # Increased wait time to avoid IP blocking
                print(f"{Fore.YELLOW}⏳ Waiting {wait_time} seconds before next playlist to avoid IP blocking...{Style.RESET_ALL}")
                time.sleep(wait_time)
        
        return self.total_success_count

    def print_summary(self):
        """Print comprehensive download summary"""
        print(f"\n{Fore.GREEN}{'='*80}{Style.RESET_ALL}")
        print(f"📊 COMPREHENSIVE DOWNLOAD SUMMARY")
        print(f"{'='*80}{Style.RESET_ALL}")
        
        print(f"{Fore.CYAN}🎯 OVERALL RESULTS:{Style.RESET_ALL}")
        print(f"✅ Total downloaded: {self.total_success_count}")
        print(f"⏭️  Total skipped: {len(self.total_skipped_videos)}")
        print(f"❌ Total failed: {len(self.total_failed_videos)}")
        
        print(f"\n{Fore.CYAN}📋 PER-PLAYLIST BREAKDOWN:{Style.RESET_ALL}")
        for result in self.playlist_results:
            status = "✅" if result['success'] > 0 else "❌"
            print(f"{status} Playlist {result['playlist_index']:2d}: {result['success']:3d} success, {result['failed']:3d} failed, {result['skipped']:3d} skipped ({result['total']:3d} total)")
        
        if self.total_failed_videos:
            print(f"\n{Fore.RED}❌ Failed Video Details (first 10):{Style.RESET_ALL}")
            for failed in self.total_failed_videos[:10]:
                print(f"  • P{failed['playlist_index']} - {failed['title']} ({failed['id']}): {failed.get('reason', 'Unknown error')}")
            if len(self.total_failed_videos) > 10:
                print(f"   ... and {len(self.total_failed_videos) - 10} more")
        
        print(f"\n{Fore.CYAN}📁 Transcripts saved to: {self.transcript_dir}/{Style.RESET_ALL}")

def main():
    """Main function"""
    print(f"{Fore.GREEN}🎬 YouTube Transcript Downloader (API Version){Style.RESET_ALL}")
    
    downloader = YouTubeTranscriptDownloader()
    playlist_urls = downloader.read_playlist_urls()
    if not playlist_urls:
        sys.exit(1)
    
    print(f"\n📋 Found {len(playlist_urls)} playlist URLs:")
    for i, url in enumerate(playlist_urls, 1):
        print(f"   {i:2d}. {url.split('&list=')[1][:40]}...")
    
    # Ask user for delay configuration
    print(f"\n{Fore.CYAN}⚙️  Rate Limiting Configuration (IP Blocking Prevention):{Style.RESET_ALL}")
    print("   • 5 seconds: Very Conservative (recommended for IP blocking)")
    print("   • 3 seconds: Conservative")
    print("   • 2 seconds: Moderate (may hit limits)")
    print("   • 1 second: Fast (high risk of IP blocking)")
    
    try:
        delay_input = input(f"\n{Fore.CYAN}⏱️  Delay between videos (seconds, default 5): {Style.RESET_ALL}").strip()
        delay_between_videos = int(delay_input) if delay_input else 5
    except (ValueError, EOFError):
        delay_between_videos = 5
        print(f"{Fore.YELLOW}⚠️  Using default 5 seconds{Style.RESET_ALL}")
    
    print(f"\n{Fore.CYAN}🎯 Download Options:{Style.RESET_ALL}")
    print("   • Start from playlist 5 (skip already downloaded 1-4)")
    print("   • Start from playlist 1 (download all)")
    
    try:
        start_option = input(f"\n{Fore.CYAN}📋 Start from playlist (default 5): {Style.RESET_ALL}").strip()
        start_from_playlist = int(start_option) if start_option else 5
    except (ValueError, EOFError):
        start_from_playlist = 5
        print(f"{Fore.YELLOW}⚠️  Using default: starting from playlist 5{Style.RESET_ALL}")
    
    remaining_playlists = len(playlist_urls) - start_from_playlist + 1
    try:
        confirm = input(f"\n{Fore.CYAN}🔍 Process {remaining_playlists} playlists (starting from {start_from_playlist}) with {delay_between_videos}s delay? (y/N): {Style.RESET_ALL}").strip().lower()
        if confirm not in ['y', 'yes']:
            print("Operation cancelled.")
            sys.exit(0)
    except EOFError:
        print(f"{Fore.YELLOW}⚠️  Auto-confirming with defaults{Style.RESET_ALL}")
        # Continue with execution
    
    try:
        downloader.download_all_playlists(delay_between_videos=delay_between_videos, start_from_playlist=start_from_playlist)
        downloader.print_summary()
        print(f"\n{Fore.GREEN}🎉 All playlists processed!{Style.RESET_ALL}")
            
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}⏹️  Operation cancelled.{Style.RESET_ALL}")
        downloader.print_summary()
    except Exception as e:
        print(f"\n{Fore.RED}❌ An unexpected error occurred: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 