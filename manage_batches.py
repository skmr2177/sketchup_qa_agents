#!/usr/bin/env python3
"""
Batch Management - View status, resume processing, etc.
"""

import json
import argparse
from pathlib import Path
from datetime import datetime
from batch_processor import BatchQAProcessor


class BatchManager:
    def __init__(self):
        self.progress_file = Path("batch_processing/batch_progress.json")
        self.transcripts_dir = Path("transcripts")
        self.output_dir = Path("output")
    
    def get_status(self):
        """Get overall processing status"""
        if not self.progress_file.exists():
            return "No processing history found"
        
        with open(self.progress_file, 'r') as f:
            progress = json.load(f)
        
        status = f"""
📊 Batch Processing Status
{'='*50}
Last Updated: {progress.get('last_updated', 'Never')}
Total Files Processed: {progress.get('total_processed', 0)}

Playlist Status:
"""
        
        # Check each playlist
        all_playlists = [d.name for d in self.transcripts_dir.iterdir() if d.is_dir()]
        
        for playlist_id in all_playlists:
            playlist_dir = self.transcripts_dir / playlist_id
            output_dir = self.output_dir / playlist_id
            
            total_files = len(list(playlist_dir.glob("*.txt")))
            processed_files = len(list(output_dir.glob("*_QnA.md"))) if output_dir.exists() else 0
            remaining = total_files - processed_files
            
            status += f"\n{playlist_id}:"
            status += f"\n  Total: {total_files}"
            status += f"\n  Processed: {processed_files}"
            status += f"\n  Remaining: {remaining}"
            
            if playlist_id in progress.get('playlists', {}):
                batches = progress['playlists'][playlist_id].get('batches_completed', 0)
                status += f"\n  Batches Completed: {batches}"
        
        return status
    
    def resume_playlist(self, playlist_id, force_regenerate=False):
        """Resume processing a specific playlist"""
        processor = BatchQAProcessor()
        playlist_path = self.transcripts_dir / playlist_id
        
        if playlist_path.exists():
            processor.process_playlist(playlist_path, force_regenerate)
        else:
            print(f"Playlist not found: {playlist_id}")
    
    def process_single_batch(self, playlist_id, batch_num, force_regenerate=False):
        """Process a specific batch"""
        processor = BatchQAProcessor()
        playlist_path = self.transcripts_dir / playlist_id
        files = sorted(list(playlist_path.glob("*.txt")))
        
        start = (batch_num - 1) * processor.batch_size
        end = min(start + processor.batch_size, len(files))
        
        if start < len(files):
            batch_files = files[start:end]
            processor.process_batch(playlist_id, batch_files, batch_num, force_regenerate)
        else:
            print(f"Batch {batch_num} exceeds file count")


def main():
    parser = argparse.ArgumentParser(description="Manage Batch Processing")
    parser.add_argument("--status", action="store_true", help="Show status")
    parser.add_argument("--resume", help="Resume playlist ID")
    parser.add_argument("--batch", type=int, help="Process specific batch")
    parser.add_argument("--playlist", help="Playlist ID for batch")
    parser.add_argument("--force", action="store_true", help="Force regenerate all Q&A files (overwrite existing)")
    
    args = parser.parse_args()
    manager = BatchManager()
    
    if args.status:
        print(manager.get_status())
    elif args.resume:
        manager.resume_playlist(args.resume, args.force)
    elif args.batch and args.playlist:
        manager.process_single_batch(args.playlist, args.batch, args.force)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()