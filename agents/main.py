import os
import re
import json
from autogen import AssistantAgent
from sentence_transformers import SentenceTransformer, util
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ======== Agent Setup ========
def create_agents():
    """Create agents with proper API key handling"""
    # Ensure environment variables are loaded
    load_dotenv()
    
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY not found. Please set it in your .env file")
    
    llm_config = {
        "model": "gpt-3.5-turbo",
        "api_key": os.getenv("OPENAI_API_KEY")
    }
    
    qa_generator = AssistantAgent(
        name="QAGenerator",
        system_message=(
            "You're a SketchUp tutorial assistant. From each transcript chunk, generate all possible unique, helpful instructional Q&A pairs. "
            "CRITICAL: Each answer must be specific to the tutorial content shown. NEVER generate generic answers that could apply to any tutorial. "
            "If a tool is mentioned but not demonstrated, acknowledge this limitation. "
            "Include specific examples, techniques, or demonstrations from the transcript. "
            "Format: Q: ..., A: ... Return only the Q&A pairs."
        ),
        llm_config=llm_config,
    )

    refiner = AssistantAgent(
        name="Refiner",
        system_message=(
            "You're a Q&A editor. Improve clarity, remove redundancy, and polish language without changing meaning. "
            "CRITICAL: Ensure answers remain specific to the tutorial content. Do not make answers generic. "
            "Preserve specific examples, techniques, and demonstrations from the original answer. "
            "Output only the refined Q&A pair."
        ),
        llm_config=llm_config,
    )
    
    return qa_generator, refiner

# ======== Helper Functions ========

def clean_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "_", name)

def chunk_text(text, max_words=300):
    words = text.split()
    return [" ".join(words[i:i+max_words]) for i in range(0, len(words), max_words)]

def generate_and_refine_qas(chunk, qa_generator, refiner):
    prompt = f"""Generate all possible useful instructional Q&A pairs from this transcript chunk.

CRITICAL REQUIREMENTS:
- Each answer must be specific to the tutorial content shown
- Include specific examples, techniques, or demonstrations mentioned
- If a tool is mentioned but not demonstrated, acknowledge this limitation
- NEVER generate generic answers that could apply to any tutorial
- Reference specific tools, features, or workflows shown in the tutorial

Transcript chunk:
{chunk}"""
    
    raw_response = qa_generator.generate_reply([{"role": "user", "content": prompt}])
    raw = raw_response.get("content", "") if isinstance(raw_response, dict) else str(raw_response)
    lines = [line.strip() for line in raw.split("\n") if line.strip()]
    qas = []
    q = ""
    for line in lines:
        if line.startswith("Q:"):
            q = line
        elif line.startswith("A:") and q:
            full = f"{q}\n{line}"
            refined_response = refiner.generate_reply([{"role": "user", "content": full}])
            refined = refined_response.get("content", "") if isinstance(refined_response, dict) else str(refined_response)
            
            # Validate that the answer is not generic
            if not is_generic_answer(refined):
                qas.append(refined)
            q = ""
    return qas

def is_generic_answer(qa_pair):
    """Check if an answer is too generic and should be filtered out"""
    generic_phrases = [
        "The Move Tool serves multiple purposes in this tutorial:",
        "• Primary Function: Perform move tool operations",
        "• Key Applications: Creating precise geometric shapes",
        "• Advanced Uses: Complex modeling operations",
        "• Integration: Working with other tools and features",
        "Step-by-step Usage:",
        "The tool serves multiple purposes",
        "Perform tool operations",
        "Creating precise geometric shapes",
        "Complex modeling operations",
        "Working with other tools and features"
    ]
    
    answer_text = qa_pair.lower()
    generic_count = sum(1 for phrase in generic_phrases if phrase.lower() in answer_text)
    
    # If more than 2 generic phrases are found, consider it generic
    return generic_count >= 2

def deduplicate_qas(qas, threshold=0.85):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings, unique, seen = [], [], []

    for qa in qas:
        question = next((l[2:].strip() for l in qa.split("\n") if l.startswith("Q:")), "")
        if not question:
            continue
        embed = model.encode(question, convert_to_tensor=True)
        if all(util.cos_sim(embed, e).item() < threshold for e in embeddings):
            unique.append(qa)
            embeddings.append(embed)
    return unique

# ======== Playlist Q&A Agent ========

def extract_playlist_id_from_url(playlist_url):
    """Extract playlist ID from YouTube playlist URL"""
    import re
    
    # Pattern to match playlist ID in various URL formats
    patterns = [
        r'list=([A-Za-z0-9_-]+)',  # Standard playlist parameter
        r'playlist\?list=([A-Za-z0-9_-]+)',  # Full playlist URL
        r'PL[A-Za-z0-9_-]+'  # Direct playlist ID
    ]
    
    for pattern in patterns:
        match = re.search(pattern, playlist_url)
        if match:
            return match.group(1) if 'list=' in pattern else match.group(0)
    
    return None

def find_playlist_transcripts(playlist_id, transcripts_dir="transcripts"):
    """Find all transcript files for a given playlist ID"""
    playlist_dir = os.path.join(transcripts_dir, playlist_id)
    
    if not os.path.exists(playlist_dir):
        print(f"❌ Playlist directory not found: {playlist_dir}")
        return []
    
    transcript_files = []
    for file in os.listdir(playlist_dir):
        if file.endswith(".txt") and file.startswith("playlist_"):
            transcript_files.append(os.path.join(playlist_dir, file))
    
    print(f"📂 Found {len(transcript_files)} transcript files in {playlist_dir}")
    return sorted(transcript_files)

def extract_video_info_from_filename(filename):
    """Extract video ID and title from transcript filename"""
    import re
    
    # Pattern: playlist_XX_video_VIDEOID_Title.txt
    pattern = r'playlist_\d+_video_([A-Za-z0-9_-]+)_(.+)\.txt'
    match = re.search(pattern, os.path.basename(filename))
    
    if match:
        video_id = match.group(1)
        title = match.group(2).replace('_', ' ')
        return video_id, title
    
    return None, None

def generate_qa_for_video(transcript_file, qa_generator, refiner):
    """Generate Q&A pairs for a single video transcript"""
    video_id, title = extract_video_info_from_filename(transcript_file)
    
    print(f"🎬 Processing: {title} (ID: {video_id})")
    
    try:
        with open(transcript_file, "r", encoding="utf-8") as f:
            transcript_text = f.read()
        
        if not transcript_text.strip():
            print(f"   ⚠️  Empty transcript for {title}")
            return None
        
        print(f"   📄 Transcript length: {len(transcript_text)} characters")
        
        # Generate Q&A pairs from transcript chunks
        all_qas = []
        chunks = chunk_text(transcript_text, max_words=400)  # Slightly larger chunks for better context
        
        for i, chunk in enumerate(chunks):
            if len(chunk.strip()) < 50:  # Skip very short chunks
                continue
                
            print(f"   🔄 Processing chunk {i+1}/{len(chunks)} ({len(chunk)} chars)")
            qas = generate_and_refine_qas(chunk, qa_generator, refiner)
            all_qas.extend(qas)
        
        # Deduplicate Q&A pairs for this video
        unique_qas = deduplicate_qas(all_qas, threshold=0.85)
        
        print(f"   ✅ Generated {len(unique_qas)} unique Q&A pairs")
        
        return {
            "video_id": video_id,
            "title": title,
            "transcript_file": os.path.basename(transcript_file),
            "qa_pairs": unique_qas,
            "total_qa_pairs": len(unique_qas)
        }
        
    except Exception as e:
        print(f"   ❌ Error processing {transcript_file}: {e}")
        return None

def run_playlist_qa_agent(playlist_url, output_dir="output"):
    """
    Main function to process existing playlist transcripts and generate Q&A pairs
    
    Agent Behavior:
    📥 Input: YouTube playlist URL
    🔎 Extract playlist ID (e.g., PL_xxxxxx)
    📂 Find local transcripts in: transcripts/PL_xxxxxx/
    🤖 Generate Q&A pairs for each transcript using an OpenAI model
    🧹 Deduplicate and refine them
    📤 Save output to: PL_xxxxxx_qas.json
    """
    print("🎯 Starting Playlist Q&A Agent...")
    print(f"📥 Input URL: {playlist_url}")
    
    # Extract playlist ID
    playlist_id = extract_playlist_id_from_url(playlist_url)
    if not playlist_id:
        print("❌ Could not extract playlist ID from URL")
        return None
    
    print(f"🔎 Extracted playlist ID: {playlist_id}")
    
    # Find playlist transcripts
    transcript_files = find_playlist_transcripts(playlist_id)
    if not transcript_files:
        print("❌ No transcript files found for this playlist")
        return None
    
    # Create agents
    try:
        qa_generator, refiner = create_agents()
        print("🤖 Agents created successfully")
    except Exception as e:
        print(f"❌ Failed to create agents: {e}")
        return None
    
    # Process each video transcript
    print(f"\n🔄 Processing {len(transcript_files)} video transcripts...")
    results = []
    successful_videos = 0
    
    for i, transcript_file in enumerate(transcript_files):
        print(f"\n📺 Video {i+1}/{len(transcript_files)}")
        
        video_result = generate_qa_for_video(transcript_file, qa_generator, refiner)
        
        if video_result:
            results.append(video_result)
            successful_videos += 1
        else:
            print(f"   ❌ Failed to process video")
    
    if not results:
        print("❌ No Q&A pairs were generated for any video")
        return None
    
    # Prepare final output
    from datetime import datetime
    
    final_output = {
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "model_used": "gpt-3.5-turbo",
            "playlist_url": playlist_url,
            "playlist_id": playlist_id,
            "total_videos_processed": len(transcript_files),
            "successful_videos": successful_videos,
            "total_qa_pairs": sum(video["total_qa_pairs"] for video in results)
        },
        "videos": results
    }
    
    # Save output
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"{playlist_id}_qas.json")
    
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(final_output, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Success! Generated Q&A pairs for {successful_videos}/{len(transcript_files)} videos")
        print(f"📤 Output saved to: {output_file}")
        print(f"📊 Total Q&A pairs generated: {final_output['metadata']['total_qa_pairs']}")
        
        return output_file
        
    except Exception as e:
        print(f"❌ Failed to save output: {e}")
        return None

# ======== Execute Agent ========

if __name__ == "__main__":
    print("🎯 SketchUp Playlist Q&A Agent")
    print("=" * 50)
    
    url = input("📥 Enter SketchUp playlist URL: ")
    run_playlist_qa_agent(url) 