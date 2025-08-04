# 🤖 Automated YouTube Q&A Generation Agent

Transform YouTube playlists into comprehensive Q&A datasets automatically using AI agents!

## 🎯 Overview

This automated agent system processes YouTube playlists and generates high-quality Q&A pairs using advanced AI techniques. Simply provide a playlist URL, and the agent will:

1. **📥 Download transcripts** from all videos in the playlist
2. **🧠 Generate Q&A pairs** using AI agents (GPT-4)
3. **🔄 Refine content** for clarity and accuracy
4. **🚫 Remove duplicates** using semantic similarity
5. **💾 Save results** to structured JSON format

## ✨ Features

- **🚀 Fully Automated**: Just provide a URL and let the agent work
- **🧩 Intelligent Chunking**: Processes large transcripts efficiently
- **🤖 AI-Powered**: Uses OpenAI GPT-4 for Q&A generation and refinement
- **🔍 Smart Deduplication**: Removes similar questions using semantic embeddings
- **📊 Progress Tracking**: Real-time progress bars and colored logging
- **🛡️ Error Handling**: Robust retry logic and graceful error handling
- **⚙️ Configurable**: Customizable settings via environment variables

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- OpenAI API key
- Internet connection

### 1. Installation

```bash
# Clone or download this project
cd task1

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

```bash
# Copy the environment template
cp env_template.txt .env

# Edit .env file and add your OpenAI API key
# Replace 'your_openai_api_key_here' with your actual API key
```

### 3. Run the Agent

```bash
python run_agent.py
```

The agent will prompt you for a YouTube playlist URL and automatically process it!

## 📁 Project Structure

```
task1/
├── run_agent.py              # Main runner script
├── requirements.txt          # Dependencies
├── env_template.txt         # Environment template
├── config.py                # Configuration management
├── utils/
│   └── logger.py            # Colored logging utility
├── agents/
│   ├── main.py              # Original script (reference)
│   └── youtube_qa_agent.py  # Main agent class
├── transcripts/             # Downloaded transcripts (auto-created)
├── output/                  # Generated Q&A files (auto-created)
└── logs/                    # Log files (auto-created)
```

## ⚙️ Configuration Options

Edit your `.env` file to customize behavior:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
MODEL_NAME=gpt-4                    # AI model to use

# Processing Configuration  
MAX_CHUNK_WORDS=300                 # Words per transcript chunk
SIMILARITY_THRESHOLD=0.85           # Duplicate detection threshold
MAX_RETRIES=3                       # Retry attempts on failure
RETRY_DELAY=5                       # Delay between retries (seconds)

# Directory Configuration
TRANSCRIPT_DIR=transcripts          # Transcript storage
OUTPUT_DIR=output                   # Results storage
LOGS_DIR=logs                       # Log storage
```

## 🎬 Example Usage

1. **Start the agent**:
   ```bash
   python run_agent.py
   ```

2. **Enter a playlist URL**:
   ```
   📥 Enter YouTube playlist URL: https://www.youtube.com/playlist?list=PLrAXtmRdnEQy5QJd8k-g5oLGY4bcjMTQS
   ```

3. **Let the agent work**:
   ```
   🚀 Initializing YouTube Q&A Agent...
   [1/4] Downloading transcripts from playlist
   [2/4] Generating Q&A pairs from transcripts  
   [3/4] Removing duplicate Q&A pairs
   [4/4] Saving results to file
   ```

4. **Get your results**:
   ```json
   {
     "metadata": {
       "playlist_url": "https://www.youtube.com/playlist?list=...",
       "generated_at": "2024-01-15T10:30:00",
       "total_qas": 127,
       "model_used": "gpt-4"
     },
     "qas": [
       "Q: How do you create a basic cube in SketchUp?\nA: To create a basic cube in SketchUp, select the Rectangle tool, draw a square on the ground plane, then use the Push/Pull tool to extrude it into a 3D cube.",
       ...
     ]
   }
   ```

## 🛠️ Advanced Usage

### Using the Agent Class Directly

```python
import asyncio
from agents.youtube_qa_agent import YouTubeQAAgent

async def main():
    agent = YouTubeQAAgent()
    
    # Process a playlist
    output_file = await agent.process_playlist(
        "https://www.youtube.com/playlist?list=YOUR_PLAYLIST_ID"
    )
    
    print(f"Results saved to: {output_file}")

asyncio.run(main())
```

### Batch Processing Multiple Playlists

```python
playlists = [
    "https://www.youtube.com/playlist?list=PLAYLIST_1",
    "https://www.youtube.com/playlist?list=PLAYLIST_2"
]

for url in playlists:
    output_file = await agent.process_playlist(url)
    print(f"Processed: {output_file}")
```

## 📊 Output Format

The agent generates structured JSON files with metadata and Q&A pairs:

```json
{
  "metadata": {
    "playlist_url": "Original playlist URL",
    "generated_at": "ISO timestamp",
    "total_qas": "Number of Q&A pairs",
    "model_used": "AI model name",
    "similarity_threshold": "Deduplication threshold"
  },
  "qas": [
    "Q: Question text\nA: Answer text",
    ...
  ]
}
```

## 🔧 Troubleshooting

### Common Issues

**Import Errors**:
```bash
pip install -r requirements.txt
```

**API Key Issues**:
- Check your `.env` file exists
- Verify your OpenAI API key is correct
- Ensure you have sufficient API credits

**No Transcripts Found**:
- Verify the playlist URL is correct and public
- Some videos may not have transcripts available
- Try a different playlist

**Memory Issues**:
- Reduce `MAX_CHUNK_WORDS` in `.env`
- Process smaller playlists
- Close other applications

### Getting Help

1. Check the logs in the `logs/` directory
2. Enable debug logging by setting log level in the config
3. Review error messages for specific guidance

## 🤝 Contributing

Feel free to improve this project:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is open source. Use it responsibly and respect YouTube's terms of service.

## 🎉 Acknowledgments

- OpenAI for providing powerful language models
- AutoGen team for the multi-agent framework
- PyTube for YouTube video access
- SentenceTransformers for semantic similarity

---

**Happy Q&A Generation! 🚀** 