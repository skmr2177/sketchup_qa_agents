# Enhanced Q&A Agent for YouTube Playlist Transcripts

## 🎯 How I Saved and Ran the Agent in Cursor (Complete Workflow)

Here's exactly how you saved and ran the agent system in Cursor to generate Q&A pairs:

### Step 1: Prepared Playlist URLs
You saved all YouTube playlist URLs in **`skecthup_playlist.txt`**:
```
https://www.youtube.com/watch?v=DMsakCycpAs&list=PL-bndkJaV8A4ofk43YYdTZaG4TJWqgOIa
https://www.youtube.com/watch?v=J8AQ2n752vE&list=PL-bndkJaV8A65rVfOEqQ7VYJc46cerIqf
https://www.youtube.com/watch?v=2oIh3iauems&list=PL-bndkJaV8A6lnfX-GTNSW64I_xa5ofQp
... (13 playlists total)
```

### Step 2: Downloaded Transcripts Using Agent
**In Cursor, you:**
1. **Referenced the playlist URLs** one by one from `skecthup_playlist.txt`
2. **Used `download_transcripts_api.py`** to download and save transcripts
3. **Asked Cursor assistant** to run the download script for each playlist

**Command used:**
```bash
python download_transcripts_api.py
```

This created transcript files like:
```
transcripts/
├── playlist_01_video_vbn07cYzrL8_3D Basecamp 2024 Keynote.txt
├── playlist_05_video_0RN7kF4vQ4M_Simple Scene Update with Apply Tags to Scenes.txt
└── ... (200+ transcript files)
```

### Step 3: Organized Videos by Playlist
**You asked Cursor to organize transcripts** under their respective playlists:
```bash
python organize_transcripts.py
```

This moved files from:
```
transcripts/playlist_05_video_xxxxx_Title.txt
```
To organized folders:
```
transcripts/PL-bndkJaV8A438k9GoBVKA5Xy3OLk_1hn/
├── video_0RN7kF4vQ4M_Simple Scene Update with Apply Tags to Scenes.txt
├── video_3e4dpdmNhik_How to 3D Model a Hot Dog in SketchUp.txt
└── ...
```

### Step 4: Created Agent Instructions in Cursor
**You saved these agent files:**
- **`agents/ENHANCED_QnAGen_agent.md`** - Detailed Q&A generation instructions
- **`agents/sample.md`** - Example showing INPUT transcript → OUTPUT Q&A format

### Step 5: Generated Q&A Using Cursor Agent
**Your process in Cursor:**

1. **Referenced the agent prompt:** Used `@ENHANCED_AGENT_README.md` and `@sample.md`
2. **Asked Cursor assistant:** "Generate Q&A pairs using these instructions"
3. **Provided transcript content** from individual video files
4. **Got Q&A output** following the sample.md format
5. **Saved to output folder** as `video_xxxxx_QnA.md` files

**Example Cursor conversation:**
```
User: "Use @ENHANCED_AGENT_README.md and reference to @sample.md to generate Q&A pairs for this transcript"
[Paste transcript content]

Cursor: "I'll generate comprehensive Q&A pairs following your agent instructions..."
[Generated Q&A pairs with proper formatting]

User: "Save this as video_xxxxx_QnA.md in the output/PL-xxxxx/ folder"
```

### Step 6: Categorized Q&A Pairs Using Web Search
**Final step in Cursor:**

1. **Used `@categorize_complete_qa_pairs.py`** for categorization
2. **Mentioned help.sketchup.com URLs** for reference categories
3. **Enabled web search** for accurate categorization
4. **Asked Cursor to categorize** all Q&A pairs by topic

**Command used:**
```bash
python categorize_complete_qa_pairs.py
```

This organized Q&A pairs into categories like:
```
output/categories/
├── 3d_modeling/3d_modeling.md
├── extensions/extensions.md
├── rendering_visualization/rendering_visualization.md
├── layout/layout.md
├── sketchup_desktop/sketchup_desktop.md
├── 3d_warehouse/3d_warehouse.md
├── troubleshooting/troubleshooting.md
└── performance/performance.md
```

### Step 7: How You Saved the Generated Q&A
After generating Q&A pairs with the agent prompt, you saved them as:
```
output/PL-bndkJaV8A438k9GoBVKA5Xy3OLk_1hn/
├── video_0RN7kF4vQ4M_Simple Scene Update with Apply Tags to Scenes_QnA.md
├── video_3e4dpdmNhik_How to 3D Model a Hot Dog in SketchUp  🌭_QnA.md
├── video_6ZqHYH2Xno0_How to 3D Model a Business Card Holder_QnA.md
└── ...
```

### Step 6: Your Q&A File Format
Each generated Q&A file followed this structure:
```markdown
# Q&A for [Video Title]

**Video ID:** [YouTube Video ID]
**Playlist Index:** [Number]
**Generated:** [Timestamp]

---

### OUTPUT Generate Q&A pairs

1. [Question 1]?
Answer:
[Detailed step-by-step answer with formatting]

2. [Question 2]?
Answer:
[Detailed answer...]

...
```

### Step 8: The Complete Cursor Workflow
**Your actual process in Cursor was:**

1. **Save playlist URLs** → `skecthup_playlist.txt` (13 playlists)
2. **Download transcripts** → `python download_transcripts_api.py` (one by one)
3. **Organize by playlist** → `python organize_transcripts.py`
4. **Create agent instructions** → `agents/ENHANCED_QnAGen_agent.md` & `sample.md`
5. **Generate Q&A in Cursor** → Using @agent prompts + transcript content
6. **Save Q&A files** → `output/PL-xxxxx/video_xxxxx_QnA.md`
7. **Categorize Q&A** → `python categorize_complete_qa_pairs.py` with web search
8. **Final organization** → `output/categories/` by topic

### Step 8: Agent Instructions You Used
From your **ENHANCED_QnAGen_agent.md**:
- **Structure:** "Number each Q&A pair sequentially (1, 2, 3, etc.)"
- **Content:** "Cover 100% of useful content mentioned in the transcript"
- **Target:** "Aim for 15-25 Q&A pairs per transcript"
- **Format:** "Use bullet points for step-by-step instructions"
- **Quality:** "Include practical tips and troubleshooting scenarios"

### Step 9: Results You Achieved
Your manual process generated:
- **93+ video Q&A files** across multiple playlists
- **Comprehensive coverage** of SketchUp tutorials
- **Consistent formatting** following your agent template
- **High-quality content** with step-by-step instructions
- **Complete answers** without "refer to transcript" placeholders

### Key Advantages of Your Manual Approach:
1. **Full control** over Q&A quality and content
2. **Custom formatting** exactly as needed
3. **No API costs** or rate limiting issues
4. **Immediate results** without complex setup
5. **Easy to verify** and edit generated content
6. **Consistent with your sample.md template**

This manual approach using the agent prompt gave you complete control over the Q&A generation process! 🎯

This system allows you to generate comprehensive Q&A pairs from YouTube playlist transcripts using manual agent prompts and TOC automation. It builds upon your existing transcript collection and provides tools for organizing and tracking your Q&A generation process.

## 🚀 Features

- **Manual Q&A Generation**: Uses agent prompts with AI assistant for full control
- **TOC Automation**: Automatically tracks transcripts and Q&A completion status
- **Playlist Organization**: Organizes files by playlist folders
- **Status Tracking**: CSV-based tracking of what's completed vs missing
- **Quality Control**: Manual process ensures high-quality, complete answers
- **No API Costs**: Uses agent prompts instead of automated API calls

## 📁 File Structure

```
task1/
├── agents/
│   ├── ENHANCED_QnAGen_agent.md   # Agent instructions for Q&A generation
│   ├── sample.md                  # Example INPUT→OUTPUT format
│   └── transcript_manager.py      # (Legacy - not used in your workflow)
├── transcripts/                   # Your existing transcript files
│   ├── PL-xxxxx/                  # Organized by playlist
│   └── ...
├── output/                        # Generated Q&A results
│   ├── PL-xxxxx/                  # Q&A files organized by playlist
│   └── categories/                # Categorized Q&A by topic
├── toc_generator.py               # TOC automation for tracking
├── toc.csv                        # Status tracking spreadsheet
├── interactive_toc.py             # Interactive TOC generation
└── skecthup_playlist.txt          # Your playlist URLs
```

## 🛠️ Setup

### 1. Install Dependencies

```bash
pip install pyautogen sentence-transformers python-dotenv
```

### 2. Set Up Environment Variables

Create a `.env` file in your project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Verify Your Transcripts

Run the test script to verify your transcripts are properly indexed:

```bash
python test_transcript_manager.py
```

This will show you:
- Total number of transcripts available
- Playlist breakdown
- Sample transcript information

## 🎯 Usage

### Basic Usage

1. **Run the Enhanced Agent**:
   ```bash
   python run_enhanced_agent.py
   ```

2. **Enter a Playlist URL**: Use one of the URLs from your `skecthup_playlist.txt` file

3. **Wait for Processing**: The agent will:
   - Index your existing transcripts
   - Find transcripts for the specified playlist
   - Generate Q&A pairs using AI
   - Save results to the `output/` directory

### Advanced Usage

You can also use the agent programmatically:

```python
from agents.enhanced_qa_agent import EnhancedQAAgent

# Create agent
agent = EnhancedQAAgent()

# Generate Q&A from a playlist
playlist_url = "https://www.youtube.com/playlist?list=PL-bndkJaV8A4ofk43YYdTZaG4TJWqgOIa"
results = agent.generate_qa_from_playlist(playlist_url, "my_results.json")

# Access results
print(f"Generated {results['metadata']['total_qas']} Q&A pairs")
for qa in results['qa_pairs']:
    print(f"Video: {qa['video_title']}")
    print(f"Q&A: {qa['qa_pair']}")
```

## 📊 Understanding Your Transcripts

The system automatically indexes your existing transcripts based on their filenames:

### Filename Patterns Supported

1. **Playlist-based naming**: `playlist_XX_video_VIDEOID_TITLE.txt`
   - Example: `playlist_13_video_M8Q5LHLD6Z8_SketchUp Skill Builder_ Tip for Editing Components.txt`

2. **Simple naming**: `video_VIDEOID_TITLE.txt`
   - Example: `video_vbn07cYzrL8_3D Basecamp 2024 Keynote.txt`

### Transcript Content Format

Your transcripts should have this structure:
```
Title: [Video Title]
Video ID: [YouTube Video ID]
URL: https://www.youtube.com/watch?v=[VIDEO_ID]
Downloaded: [Timestamp]
--------------------

[Transcript content here...]
```

## 🔧 How It Works

### 1. Transcript Indexing
- Scans the `transcripts/` directory
- Extracts video information from filenames
- Builds an index for quick lookup

### 2. Playlist Mapping
- Extracts playlist ID from YouTube URLs
- Maps playlist URLs to corresponding transcript files
- Handles multiple playlists efficiently

### 3. Q&A Generation
- Chunks transcript content into manageable pieces
- Uses GPT-3.5-turbo to generate instructional Q&A pairs
- Refines Q&A pairs for clarity and accuracy
- Removes duplicates using semantic similarity

### 4. Output Format

Generated Q&A files contain:
```json
{
  "metadata": {
    "generated_at": "2024-01-15T10:30:00",
    "playlist_url": "https://www.youtube.com/playlist?list=...",
    "total_qas": 25,
    "videos_processed": 8,
    "model_used": "gpt-3.5-turbo"
  },
  "qa_pairs": [
    {
      "video_id": "M8Q5LHLD6Z8",
      "video_title": "SketchUp Skill Builder: Tip for Editing Components",
      "qa_pair": "Q: How do I edit components in SketchUp?\nA: To edit components...",
      "playlist_url": "https://www.youtube.com/playlist?list=..."
    }
  ]
}
```

## 🎯 Example Workflow

1. **Check Available Transcripts**:
   ```bash
   python test_transcript_manager.py
   ```

2. **Generate Q&A for a Playlist**:
   ```bash
   python run_enhanced_agent.py
   # Enter: https://www.youtube.com/playlist?list=PL-bndkJaV8A4ofk43YYdTZaG4TJWqgOIa
   ```

3. **Review Results**:
   - Check the generated JSON file in `output/`
   - Review Q&A pairs for quality
   - Use the content for your instructional materials

## 🔍 Troubleshooting

### Common Issues

1. **"No transcripts found"**
   - Run `python test_transcript_manager.py` to verify indexing
   - Check that transcript files are in the `transcripts/` directory
   - Ensure filenames follow the expected patterns

2. **"No Q&A pairs generated"**
   - Check your OpenAI API key in `.env`
   - Verify transcripts have sufficient content (>100 characters)
   - Check for API rate limiting

3. **Import errors**
   - Ensure all dependencies are installed
   - Check that the `agents/` directory exists
   - Verify Python path includes the project directory

### Debugging

- Use `test_transcript_manager.py` to verify transcript indexing
- Check the console output for detailed error messages
- Review the generated JSON files for partial results

## 📈 Performance Tips

1. **Batch Processing**: Process multiple playlists in sequence
2. **Rate Limiting**: The system includes built-in delays to avoid API limits
3. **Content Quality**: Longer, more detailed transcripts generate better Q&A pairs
4. **Deduplication**: The system automatically removes similar Q&A pairs

## 🔄 Integration with Existing Workflow

This enhanced system works alongside your existing scripts:

- **Download Scripts**: Continue using `download_playlist_transcripts.py` for new transcripts
- **Original Agent**: Your `agents/main.py` is still available for comparison
- **Existing Transcripts**: All your current transcripts are automatically indexed

## 🎉 Benefits

- **Efficiency**: Uses existing transcripts instead of re-downloading
- **Quality**: AI-generated Q&A pairs are more comprehensive and accurate
- **Scalability**: Can handle multiple playlists and large transcript collections
- **Flexibility**: Easy to customize and extend for different use cases

## 📞 Support

If you encounter issues:

1. Run the test script to verify setup
2. Check the console output for error messages
3. Verify your OpenAI API key and quota
4. Ensure all dependencies are properly installed

The enhanced system provides a powerful foundation for generating instructional Q&A content from your YouTube playlist transcripts! 