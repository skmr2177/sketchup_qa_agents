import os
import requests
import sys
import re
import time

TRANSCRIPTS_DIR = 'transcripts'
OUTPUT_DIR = 'output'
PROMPT_PATH = 'agents/ENHANCED_QnAGen_agent.md'
OLLAMA_MODEL = 'llama3.2:3b'  # Change to your preferred local model name

def clean_transcript_text(text):
    """Remove instructor names and personal references from transcript text"""
    if not text:
        return text
    
    # Common instructor names to remove (add more as needed)
    instructor_names = [
        'Eric', 'Aaron', 'Sam', 'Mike', 'John', 'David', 'Chris', 'Tom', 'Steve', 'Danny',
        'eric', 'aaron', 'sam', 'mike', 'john', 'david', 'chris', 'tom', 'steve', 'danny'
    ]
    
    # Remove instructor names
    for name in instructor_names:
        text = re.sub(rf'\b{name}\b', '', text, flags=re.IGNORECASE)
    
    # Remove phrases that reference the instructor
    instructor_phrases = [
        r'the instructor',
        r'your instructor',
        r'our instructor',
        r'the presenter',
        r'the teacher',
        r'the host',
        r'your teacher',
        r'our teacher',
        r'the speaker',
        r'the demonstrator',
        r'the trainer'
    ]
    
    for phrase in instructor_phrases:
        text = re.sub(phrase, '', text, flags=re.IGNORECASE)
    
    # Remove personal pronouns that might refer to instructor
    personal_refs = [
        r'\bI\'m\b',
        r'\bI am\b',
        r'\bI\'ll\b',
        r'\bI will\b',
        r'\bI\'ve\b',
        r'\bI have\b',
        r'\bmy\b',
        r'\bme\b',
        r'\bI\'d\b',
        r'\bI would\b',
        r'\bI could\b',
        r'\bI should\b'
    ]
    
    for ref in personal_refs:
        text = re.sub(ref, '', text, flags=re.IGNORECASE)
    
    # Clean up extra whitespace
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    return text

def check_ollama_connection():
    """Check if Ollama is running and accessible"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama is running and accessible")
            return True
    except requests.exceptions.ConnectionError:
        print("❌ Error: Ollama is not running or not accessible")
        print("Please start Ollama by running: ollama serve")
        print("Or install Ollama from: https://ollama.com/")
        return False
    except Exception as e:
        print(f"❌ Error checking Ollama: {e}")
        return False

def get_prompt():
    try:
        with open(PROMPT_PATH, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"❌ Error: Could not find prompt file at {PROMPT_PATH}")
        sys.exit(1)

def generate_qa_ollama(transcript_text, filename):
    """Generate Q&A pairs using Ollama with enhanced error handling and chunking"""
    
    # Process transcript in chunks if it's too long
    max_chars = 25000  # Increased limit for better coverage
    if len(transcript_text) > max_chars:
        print(f"   ⚠️  Transcript too long ({len(transcript_text)} chars), processing in chunks")
        return process_transcript_in_chunks(transcript_text, filename, max_chars)
    
    return process_single_chunk(transcript_text, filename)

def process_transcript_in_chunks(transcript_text, filename, max_chars):
    """Process long transcripts by splitting into overlapping chunks"""
    chunks = []
    overlap = 5000  # Overlap between chunks to maintain context
    
    # Split transcript into overlapping chunks
    start = 0
    while start < len(transcript_text):
        end = min(start + max_chars, len(transcript_text))
        chunk = transcript_text[start:end]
        chunks.append(chunk)
        start = end - overlap
        if start >= len(transcript_text):
            break
    
    print(f"   📄 Processing {len(chunks)} chunks...")
    
    all_qa_content = []
    for i, chunk in enumerate(chunks):
        print(f"   📝 Processing chunk {i+1}/{len(chunks)}...")
        qa_content = process_single_chunk(chunk, filename, chunk_info=f" (chunk {i+1}/{len(chunks)})")
        if qa_content:
            all_qa_content.append(qa_content)
    
    # Combine all Q&A content
    if all_qa_content:
        combined_content = "\n\n".join(all_qa_content)
        return combined_content
    return None

def process_single_chunk(transcript_text, filename, chunk_info=""):
    """Process a single chunk of transcript text"""
    
    # Compose the full prompt for the model
    full_prompt = (
        "# Enhanced Q&A Generation Agent\n\n"
        "You are an AI agent specialized in generating complete, accurate answers to questions derived from SketchUp tutorial transcripts.\n\n"
        "## 🎯 Your Objective\n"
        "Answer every extracted question with a complete, accurate, and tutorial-specific response.\n\n"
        "**Use only the transcript as the primary source.**\n\n"
        "You may optionally enhance your answer with knowledge from SketchUp Help Center (https://help.sketchup.com) but only if:\n"
        "- It supplements what's already in the transcript\n"
        "- It helps clarify terminology, keyboard shortcuts, or best practices used in the tutorial\n"
        "- It does not contradict or generalize beyond the actual steps shown in the video\n\n"
        "## 🧾 Input\n"
        "Extract from transcripts\n\n"
        "## 🧠 Instructions\n"
        "For each question:\n\n"
        "1. **Locate the relevant answer in the transcript**\n"
        "2. **Only answer if the transcript actually covers the topic**\n"
        "3. **Be honest: say \"This topic is not covered in this tutorial\" if needed**\n"
        "4. **Answer in a clear, actionable, and specific way:**\n"
        "   - Include the tool/method used\n"
        "   - Describe on-screen steps or UI interactions\n"
        "   - **NEVER mention instructor names (Eric, Aaron, Sam, etc.)**\n"
        "   - **Make answers question-specific without personal references**\n"
        "   - Mention keyboard shortcuts or efficiency tips only if used in the video\n"
        "   - **Use different writing styles and approaches for each answer**\n\n"
        "5. **Enhance your answer using SketchUp Help content only when appropriate:**\n"
        "   - If a concept or tool is used but not clearly explained, refer to official Help docs only to support the answer, not replace it\n\n"
        "6. **Ensure answer uniqueness:**\n"
        "   - **Never repeat the same explanation pattern** across different questions\n"
        "   - **Vary your vocabulary and sentence structure** for each answer\n"
        "   - **Use different examples and references** from the transcript for each question\n"
        "   - **Make each answer feel distinct and original**\n\n"
        "## 🚫 Strict Don'ts\n"
        "❌ Don't write answers based only on Help documentation\n"
        "❌ Don't fabricate features or workflows not shown in the video\n"
        "❌ Don't use copy-paste boilerplate answers across different tutorials\n"
        "❌ Don't make up steps that aren't visible in the transcript\n"
        "❌ Don't repeat the same answer structure or content for different questions\n"
        "❌ Don't use generic templates that could apply to multiple questions\n"
        "❌ Don't copy-paste similar explanations across different Q&A pairs\n"
        "❌ **NEVER mention instructor names (Eric, Aaron, Sam, etc.)**\n"
        "❌ **Don't use phrases like \"the instructor shows\" or \"Aaron demonstrates\"**\n"
        "❌ **Don't use phrases like \"the tutorial shows\" or \"this video demonstrates\"**\n"
        "❌ **Don't reference who is teaching or presenting the content**\n"
        "❌ **Don't use personal pronouns referring to the instructor**\n"
        "❌ **Don't use \"I\", \"my\", \"me\" or any first-person references**\n"
        "❌ **Don't mention who created or presented the tutorial**\n"
        "❌ **Don't reference the speaker or presenter in any way**\n\n"
        "## ✅ Output\n"
        "For each question, provide:\n"
        "- A full answer grounded in the tutorial transcript\n"
        "- Supplemented (if helpful) with clarifying info from SketchUp Help Docs\n"
        "- **Question-specific answers without personal references**\n"
        "- **Generic, content-focused language that doesn't reference who taught it**\n"
        "- **Pure technical descriptions without any personal context**\n\n"
        "### Example:\n"
        "**Q:** How is the Follow Me tool used in this tutorial?\n"
        "**A:** The Follow Me tool is used to extrude a curved profile along a circular path to create crown molding. The process involves selecting the path first, then clicking the profile. While the tool is used efficiently, it is not explained in detail. According to SketchUp Help, the Follow Me tool works by extruding a face along a preselected path.\n\n"
        "## 📌 File Output\n"
        "Save your results in Markdown under `output/{original_transcript_name}_QnA.md`\n\n"
        "## Structure Requirements\n\n"
        "## Reference Format\n\n"
        "##INPUT TRANSCRIPT\n\n"
        "Below is a transcript that has been pre-cleaned to remove instructor names and personal references. Generate Q&A pairs as per the above instructions. "
        "**CRITICAL: The transcript has been cleaned of instructor names. Do not reference any person, instructor, presenter, or speaker. Make questions and answers purely technical and content-focused. Focus entirely on SketchUp techniques, tools, and methods being covered. Use only third-person descriptions of the techniques.**\n\n"
        "TRANSCRIPT:\n"
        f"{transcript_text}\n\n"
        "Q&A PAIRS:\n"
    )
    
    try:
        print(f"   ⏳ Sending request to Ollama (timeout: 10 minutes)...")
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": full_prompt,
                "stream": False
            },
            timeout=600  # Increased to 10 minutes
        )
        response.raise_for_status()
        return response.json()['response']
    except requests.exceptions.ConnectionError:
        print(f"   ❌ Error: Cannot connect to Ollama. Make sure it's running on localhost:11434")
        return None
    except requests.exceptions.Timeout:
        print(f"   ❌ Error: Request timed out after 10 minutes. The model might be too slow for this transcript size.")
        return None
    except Exception as e:
        print(f"   ❌ Error generating Q&A: {e}")
        return None

def process_all():
    # Check if Ollama is running first
    if not check_ollama_connection():
        return
    
    processed_count = 0
    error_count = 0
    total_files = 0
    
    print(f"📁 Scanning transcripts in: {TRANSCRIPTS_DIR}")
    
    # First, count total files
    for root, dirs, files in os.walk(TRANSCRIPTS_DIR):
        for file in files:
            if file.endswith('.txt'):
                total_files += 1
    
    print(f"📊 Found {total_files} transcript files to process")
    
    current_file = 0
    for root, dirs, files in os.walk(TRANSCRIPTS_DIR):
        for file in files:
            if file.endswith('.txt'):
                current_file += 1
                transcript_path = os.path.join(root, file)
                
                print(f"\n🔄 Processing file {current_file}/{total_files}: {file}")
                
                try:
                    with open(transcript_path, 'r', encoding='utf-8') as f:
                        transcript_text = f.read()
                    
                    # Clean the transcript text to remove personal references
                    transcript_text = clean_transcript_text(transcript_text)

                    # Build output path
                    rel_path = os.path.relpath(transcript_path, TRANSCRIPTS_DIR)
                    base_name = os.path.splitext(os.path.basename(file))[0]
                    
                    # Handle files in root directory vs subdirectories
                    if os.path.dirname(transcript_path) == TRANSCRIPTS_DIR:
                        # File is in root transcripts directory
                        output_dir = OUTPUT_DIR
                        os.makedirs(output_dir, exist_ok=True)
                        output_path = os.path.join(output_dir, f"{base_name}_QnA.md")
                    else:
                        # File is in a playlist subdirectory
                        playlist_id = rel_path.split(os.sep)[0]
                        output_dir = os.path.join(OUTPUT_DIR, playlist_id)
                        os.makedirs(output_dir, exist_ok=True)
                        output_path = os.path.join(output_dir, f"{base_name}_QnA.md")
                    
                    # Generate and save Q&A
                    qa_content = generate_qa_ollama(transcript_text, file)
                    
                    if qa_content:
                        with open(output_path, 'w', encoding='utf-8') as out_f:
                            out_f.write(qa_content)
                        print(f"   💾 Saved: {output_path}")
                        processed_count += 1
                    else:
                        print(f"   ❌ Failed to generate Q&A for: {output_path}")
                        error_count += 1
                        
                except Exception as e:
                    print(f"   ❌ Error processing {file}: {e}")
                    error_count += 1
    
    print(f"\n📊 Summary:")
    print(f"   ✅ Successfully processed: {processed_count} files")
    print(f"   ❌ Errors: {error_count} files")
    print(f"   📁 Total files found: {total_files}")

if __name__ == '__main__':
    process_all() 