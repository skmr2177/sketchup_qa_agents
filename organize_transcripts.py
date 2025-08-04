#!/usr/bin/env python3
"""
Organize Transcript Files and Remove Duplicates
==============================================

This script finds transcript files outside the transcripts folder,
moves them into the proper structure, and removes any duplicates.
"""

import os
import shutil
import re
from typing import Dict, List, Set
from datetime import datetime

def extract_video_info_from_filename(filename: str) -> Dict:
    """Extract video information from filename"""
    # Pattern: playlist_XX_video_VIDEOID_TITLE.txt
    pattern = r'playlist_(\d+)_video_([a-zA-Z0-9_-]+)_(.+)\.txt'
    match = re.match(pattern, filename)
    
    if match:
        return {
            'playlist_index': int(match.group(1)),
            'video_id': match.group(2),
            'title': match.group(3),
            'filename': filename
        }
    return None

def get_playlist_folder_name(playlist_index: int) -> str:
    """Get the playlist folder name based on index"""
    playlist_mapping = {
        1: "PL-bndkJaV8A4ofk43YYdTZaG4TJWqgOIa",
        2: "PL-bndkJaV8A65rVfOEqQ7VYJc46cerIqf", 
        3: "PL-bndkJaV8A6lnfX-GTNSW64I_xa5ofQp",
        4: "PL-bndkJaV8A7fQttkdQ2sTfLjZxI5UeS2",
        5: "PL-bndkJaV8A438k9GoBVKA5Xy3OLk_1hn",
        6: "PL-bndkJaV8A7FiNCukanBSpxK3lIFG2KK",
        7: "PL-bndkJaV8A7sd2bapTWyre5XcJ8_0jQJ",
        8: "PL-bndkJaV8A7R2t970OmHY6kPGJwTfGP2",
        9: "PL-bndkJaV8A7da0R0SEEfb9DKMtCyMF_E",
        10: "PL-bndkJaV8A5U5nTBIp9qWmGQrzcKNJSZ",
        11: "PL-bndkJaV8A79QCvqQSeMF5pdriCU7ZC6",
        12: "PL-bndkJaV8A5lpn6Nn8ctOBbd0cVrHEE8",
        13: "PL-bndkJaV8A5VmrwvxMw-IYgSJLlV-vjH"
    }
    return playlist_mapping.get(playlist_index, f"PL-unknown-{playlist_index}")

def find_transcript_files_outside_transcripts_folder() -> List[str]:
    """Find all transcript files outside the transcripts folder"""
    transcript_files = []
    
    # Look in current directory and subdirectories (excluding transcripts folder)
    for root, dirs, files in os.walk('.'):
        # Skip the transcripts folder and its subdirectories
        if 'transcripts' in root and root != '.':
            continue
            
        for file in files:
            if file.startswith('playlist_') and file.endswith('.txt'):
                filepath = os.path.join(root, file)
                transcript_files.append(filepath)
    
    return transcript_files

def organize_transcripts():
    """Organize all transcript files and remove duplicates"""
    print("🧹 Organizing transcript files and removing duplicates...")
    
    transcript_dir = "transcripts"
    
    # Create transcripts directory if it doesn't exist
    os.makedirs(transcript_dir, exist_ok=True)
    
    # Find files outside transcripts folder
    print("🔍 Searching for transcript files outside transcripts folder...")
    outside_files = find_transcript_files_outside_transcripts_folder()
    print(f"📁 Found {len(outside_files)} transcript files outside transcripts folder")
    
    # Get all files in transcripts directory
    inside_files = []
    if os.path.exists(transcript_dir):
        for root, dirs, files in os.walk(transcript_dir):
            for file in files:
                if file.endswith('.txt'):
                    filepath = os.path.join(root, file)
                    inside_files.append(filepath)
    
    print(f"📁 Found {len(inside_files)} transcript files inside transcripts folder")
    
    # Combine all files
    all_files = outside_files + inside_files
    print(f"📁 Total files to process: {len(all_files)}")
    
    # Process files and organize them
    organized_files = {}
    duplicates_found = []
    files_moved = 0
    
    for filepath in all_files:
        filename = os.path.basename(filepath)
        video_info = extract_video_info_from_filename(filename)
        
        if not video_info:
            print(f"⚠️  Skipping file with unknown format: {filename}")
            continue
        
        video_id = video_info['video_id']
        playlist_index = video_info['playlist_index']
        
        # Check if we already have this video_id
        if video_id in organized_files:
            existing_file = organized_files[video_id]['filepath']
            existing_size = os.path.getsize(existing_file)
            current_size = os.path.getsize(filepath)
            
            # Keep the larger file (more complete transcript)
            if current_size > existing_size:
                print(f"🔄 Replacing duplicate {video_id} with larger file")
                duplicates_found.append(existing_file)
                organized_files[video_id] = {
                    'filepath': filepath,
                    'playlist_index': playlist_index,
                    'filename': filename,
                    'size': current_size
                }
            else:
                print(f"🗑️  Removing smaller duplicate: {filename}")
                duplicates_found.append(filepath)
        else:
            organized_files[video_id] = {
                'filepath': filepath,
                'playlist_index': playlist_index,
                'filename': filename,
                'size': os.path.getsize(filepath)
            }
    
    print(f"\n📊 Organization Summary:")
    print(f"   📁 Total files found: {len(all_files)}")
    print(f"   🗑️  Duplicates to remove: {len(duplicates_found)}")
    print(f"   ✅ Unique files to organize: {len(organized_files)}")
    
    # Remove duplicates
    print(f"\n🗑️  Removing duplicate files...")
    for duplicate_file in duplicates_found:
        try:
            os.remove(duplicate_file)
            print(f"   ✅ Removed: {os.path.basename(duplicate_file)}")
        except Exception as e:
            print(f"   ❌ Failed to remove {duplicate_file}: {e}")
    
    # Organize files into playlist folders
    print(f"\n📂 Organizing files into playlist folders...")
    
    for video_id, info in organized_files.items():
        filepath = info['filepath']
        playlist_index = info['playlist_index']
        filename = info['filename']
        
        # Get playlist folder name
        playlist_folder = get_playlist_folder_name(playlist_index)
        playlist_dir = os.path.join(transcript_dir, playlist_folder)
        
        # Create playlist directory if it doesn't exist
        os.makedirs(playlist_dir, exist_ok=True)
        
        # Create new filename for organized structure
        new_filename = f"video_{video_id}_{info['filename'].split('_', 3)[3]}"  # Remove playlist prefix
        new_filepath = os.path.join(playlist_dir, new_filename)
        
        # Move file to organized location
        try:
            if filepath != new_filepath:  # Only move if different location
                shutil.move(filepath, new_filepath)
                files_moved += 1
                print(f"   📁 Moved: {filename} → {playlist_folder}/{new_filename}")
        except Exception as e:
            print(f"   ❌ Failed to move {filename}: {e}")
    
    print(f"\n✅ Organization Complete!")
    print(f"   📁 Files moved: {files_moved}")
    print(f"   🗑️  Duplicates removed: {len(duplicates_found)}")
    print(f"   📂 Organized into {len(set(info['playlist_index'] for info in organized_files.values()))} playlist folders")
    
    # Show final structure
    print(f"\n📋 Final Structure:")
    for playlist_index in sorted(set(info['playlist_index'] for info in organized_files.values())):
        playlist_folder = get_playlist_folder_name(playlist_index)
        playlist_dir = os.path.join(transcript_dir, playlist_folder)
        if os.path.exists(playlist_dir):
            file_count = len([f for f in os.listdir(playlist_dir) if f.endswith('.txt')])
            print(f"   📁 Playlist {playlist_index} ({playlist_folder}): {file_count} files")

if __name__ == "__main__":
    organize_transcripts() 