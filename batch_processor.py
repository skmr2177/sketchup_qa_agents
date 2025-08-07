#!/usr/bin/env python3
"""
Batch Processor for Q&A Generation
Processes all playlists in batches of 10 files
"""

import os
import json
import time
import boto3
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import logging
from config import AWS_CONFIG, BEDROCK_CONFIG, BATCH_CONFIG

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('batch_processing.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class BatchQAProcessor:
    """Process all playlists in configurable batches"""
    
    def __init__(self):
        # Initialize Bedrock client
        self.bedrock = boto3.client(
            'bedrock-runtime',
            **AWS_CONFIG
        )
        self.model_id = BEDROCK_CONFIG["model_id"]
        
        # Batch configuration
        self.batch_size = BATCH_CONFIG["batch_size"]
        self.rate_limit = BATCH_CONFIG["rate_limit_delay"]
        
        # Progress tracking
        self.progress_dir = Path("batch_processing")
        self.progress_dir.mkdir(exist_ok=True)
        self.progress_file = self.progress_dir / "batch_progress.json"
        self.progress = self.load_progress()
    
    def load_progress(self):
        """Load progress tracking"""
        if self.progress_file.exists():
            try:
                with open(self.progress_file, 'r') as f:
                    progress = json.load(f)
                    # Ensure all required keys exist
                    if "playlists" not in progress:
                        progress["playlists"] = {}
                    if "total_processed" not in progress:
                        progress["total_processed"] = 0
                    if "last_updated" not in progress:
                        progress["last_updated"] = None
                    return progress
            except (json.JSONDecodeError, FileNotFoundError):
                pass
        return {
            "playlists": {},
            "total_processed": 0,
            "last_updated": None
        }
    
    def save_progress(self):
        """Save progress"""
        self.progress["last_updated"] = datetime.now().isoformat()
        with open(self.progress_file, 'w') as f:
            json.dump(self.progress, f, indent=2)
    
    def get_all_playlists(self):
        """Get all playlist directories"""
        transcripts_dir = Path("transcripts")
        return [d for d in transcripts_dir.iterdir() if d.is_dir() and d.name.startswith("PL-")]
    
    def process_batch(self, playlist_id, batch_files, batch_num, force_regenerate=False):
        """Process a batch of 10 files"""
        output_dir = Path("output") / playlist_id
        output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"\nProcessing Batch {batch_num} for {playlist_id}")
        logger.info(f"Files: {len(batch_files)}")
        
        results = {"success": 0, "failed": 0}
        
        for i, file_path in enumerate(batch_files, 1):
            try:
                logger.info(f"[{i}/{len(batch_files)}] {file_path.name}")
                
                # Check if already processed (unless force regenerate)
                output_file = output_dir / f"{file_path.stem}_QnA.md"
                if output_file.exists() and not force_regenerate:
                    logger.info("  [SKIP] Already exists")
                    continue
                
                # Process file
                if self.process_single_file(file_path, output_dir):
                    results["success"] += 1
                    logger.info("  [SUCCESS] Generated")
                else:
                    results["failed"] += 1
                    logger.info("  [FAILED] Generation failed")
                
                # Rate limiting
                if i < len(batch_files):
                    time.sleep(self.rate_limit)
                    
            except Exception as e:
                logger.error(f"  [ERROR] {e}")
                results["failed"] += 1
        
        # Update progress
        if "playlists" not in self.progress:
            self.progress["playlists"] = {}
            
        if playlist_id not in self.progress["playlists"]:
            self.progress["playlists"][playlist_id] = {
                "batches_completed": 0,
                "files_processed": 0
            }
        
        self.progress["playlists"][playlist_id]["batches_completed"] += 1
        self.progress["playlists"][playlist_id]["files_processed"] += results["success"]
        self.progress["total_processed"] += results["success"]
        self.save_progress()
        
        return results
    
    def process_single_file(self, file_path, output_dir):
        """Process single transcript"""
        # Read transcript
        with open(file_path, 'r', encoding='utf-8') as f:
            transcript = f.read()
        
        # Extract title
        parts = file_path.stem.split('_', 2)
        title = parts[2].replace('_', ' ') if len(parts) >= 3 else file_path.stem
        
        # Generate Q&A
        qa_content = self.generate_qa(transcript, title)
        
        if qa_content:
            # Save output
            output_file = output_dir / f"{file_path.stem}_QnA.md"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"""# {title} - Q&A

{qa_content}

---
*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
""")
            return True
        return False
    
    def generate_qa(self, transcript, title):
        """Generate Q&A using Bedrock"""
        prompt = f"""Generate comprehensive Q&A covering 100% of this tutorial content.

Title: {title}

Requirements:
1. Cover ALL content taught - be thorough and comprehensive
2. Be specific to THIS tutorial
3. Include every technique, tool, and tip mentioned
4. Number questions sequentially
5. Provide detailed answers for each question
6. Format as Q&A pairs with clear question and answer structure
7. Include questions about specific tools, extensions, workflows, and processes mentioned
8. Generate as many questions as needed to cover ALL content completely

Format your response as:
Q1. [Question]
A1. [Detailed answer]

Q2. [Question]
A2. [Detailed answer]

And so on...

CRITICAL: This tutorial contains extensive content. You MUST generate enough questions to cover EVERYTHING mentioned. Do NOT stop at 10 questions. Generate 25-40 questions or more if needed to cover all content comprehensively. Include questions about:
- Every tool and extension mentioned
- Every workflow and process described
- Every technique and tip shared
- Every case study and example
- Every integration and software mentioned
- Every challenge and solution discussed

Be exhaustive in your coverage. The transcript is long and detailed - your Q&A should reflect that depth.

Transcript:
{transcript}

Generate comprehensive Q&A with both questions and detailed answers covering ALL content:"""
        
        try:
            response = self.bedrock.invoke_model(
                modelId=self.model_id,
                contentType="application/json",
                body=json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": BEDROCK_CONFIG["max_tokens"],
                    "temperature": BEDROCK_CONFIG["temperature"],
                    "messages": [{"role": "user", "content": prompt}]
                })
            )
            
            result = json.loads(response['body'].read())
            if 'content' in result:
                return result['content'][0]['text']
                
        except Exception as e:
            logger.error(f"Bedrock error: {e}")
        
        return None
    
    def process_playlist(self, playlist_path, force_regenerate=False):
        """Process entire playlist in batches"""
        playlist_id = playlist_path.name
        files = sorted(list(playlist_path.glob("*.txt")))
        
        if not files:
            logger.info(f"No files in {playlist_id}")
            return
        
        total_batches = (len(files) + self.batch_size - 1) // self.batch_size
        
        print(f"\n{'='*60}")
        print(f"📁 Playlist: {playlist_id}")
        print(f"📄 Total files: {len(files)}")
        print(f"📦 Total batches: {total_batches}")
        if force_regenerate:
            print(f" Force regenerate: ON")
        print(f"{'='*60}")
        
        # Process in batches
        for batch_num in range(1, total_batches + 1):
            start = (batch_num - 1) * self.batch_size
            end = min(start + self.batch_size, len(files))
            batch_files = files[start:end]
            
            self.process_batch(playlist_id, batch_files, batch_num, force_regenerate)
    
    def process_all_playlists(self, force_regenerate=False):
        """Process all playlists"""
        playlists = self.get_all_playlists()
        
        print(f"\n🎯 Found {len(playlists)} playlists")
        if force_regenerate:
            print(f"🔄 Force regenerate: ON")
        
        for playlist in playlists:
            self.process_playlist(playlist, force_regenerate)
        
        print(f"\n✅ Complete! Processed {self.progress['total_processed']} files")
    
    def process_specific_playlist(self, playlist_id, force_regenerate=False):
        """Process a specific playlist by ID"""
        transcripts_dir = Path("transcripts")
        playlist_path = transcripts_dir / playlist_id
        
        if not playlist_path.exists():
            print(f"❌ Playlist {playlist_id} not found!")
            return
        
        print(f"\n🎯 Processing specific playlist: {playlist_id}")
        if force_regenerate:
            print(f"🔄 Force regenerate: ON")
        self.process_playlist(playlist_path, force_regenerate)
        print(f"\n✅ Complete! Processed {self.progress['total_processed']} files")


def main():
    parser = argparse.ArgumentParser(description='Batch Processor for Q&A Generation')
    parser.add_argument('--playlist', type=str, help='Process specific playlist ID (e.g., PL-bndkJaV8A4ofk43YYdTZaG4TJWqgOIa)')
    parser.add_argument('--force', action='store_true', help='Force regenerate all Q&A files (overwrite existing)')
    
    args = parser.parse_args()
    
    processor = BatchQAProcessor()
    
    if args.playlist:
        processor.process_specific_playlist(args.playlist, args.force)
    else:
        processor.process_all_playlists(args.force)


if __name__ == "__main__":
    main()