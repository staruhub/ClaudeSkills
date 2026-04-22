---
name: Geek-skills-podcast-generator
version: 1.0.0
description: Generate AI podcasts using Volcano Engine's Podcast AI Model. Use when user wants to create podcast audio from text input, generate conversational audio content, or transform written content into multi-speaker podcast format. Supports Chinese dual-speaker podcasts with customizable voice options.
---

# Podcast Generator

## Overview

Generate professional AI-powered podcasts using Volcano Engine's Podcast AI Model. This skill transforms text input into engaging dual-speaker podcast audio with natural conversation flow, supporting multiple audio formats and voice customization.

## Quick Start

To generate a podcast:

1. Ensure Volcano Engine credentials are available (APP_ID and ACCESS_KEY)
2. Prepare the podcast topic/content text (up to 25,000 characters)
3. Run the generation script with required parameters
4. Receive the output audio file in your preferred format

## Core Workflow

### Step 1: Prepare Input

**Required information:**
- Podcast topic or content text (Chinese, up to 25k characters)
- Volcano Engine APP ID
- Volcano Engine Access Key

**Optional customization:**
- Audio format (mp3, ogg_opus, pcm, aac)
- Sample rate (default: 24000 Hz)
- Speech rate (-50 to 100, where 100 = 2.0x speed)
- Speaker voices (default: male + female duo)
- Opening music (default: disabled)

### Step 2: Generate Podcast

Run the generation script:

```bash
python scripts/generate_podcast.py \
  --text "Your podcast topic or content" \
  --output "/path/to/output.mp3" \
  --app-id "YOUR_APP_ID" \
  --access-key "YOUR_ACCESS_KEY" \
  --format mp3 \
  --sample-rate 24000 \
  --speech-rate 0
```

**Alternative: Use as Python module**

```python
import asyncio
from scripts.generate_podcast import PodcastGenerator

async def create_podcast():
    generator = PodcastGenerator(
        app_id="YOUR_APP_ID",
        access_key="YOUR_ACCESS_KEY"
    )
    
    result = await generator.generate_podcast(
        input_text="分析下当前的大模型发展",
        output_path="podcast.mp3",
        audio_format="mp3",
        sample_rate=24000,
        speech_rate=0,
        use_head_music=False
    )
    
    if result['success']:
        print(f"✅ Podcast generated: {result['output_path']}")
    else:
        print(f"❌ Failed: {result['error']}")

asyncio.run(create_podcast())
```

### Step 3: Handle Output

The script will:
- Stream audio data in real-time
- Display progress for each speaking round
- Save the complete audio file to the specified path
- Return generation statistics (file size, round count, etc.)

## Advanced Features

### Resume from Interruption

If generation is interrupted, use the resume capability:

```python
result = await generator.generate_podcast(
    input_text="Your topic",
    output_path="podcast.mp3",
    retry_info={
        "retry_task_id": "previous_task_id",
        "last_finished_round_id": 5
    }
)
```

The system will continue from the last completed round instead of starting over.

### Custom Speaker Configuration

Specify different speaker voices:

```python
result = await generator.generate_podcast(
    input_text="Your topic",
    output_path="podcast.mp3",
    speakers=[
        "zh_male_dayixiansheng_v2_saturn_bigtts",
        "zh_female_mizaitongxue_v2_saturn_bigtts"
    ]
)
```

### Audio Format Options

Supported formats and use cases:

- **mp3**: Best for general distribution (compressed, widely supported)
- **ogg_opus**: High quality with good compression
- **pcm**: Uncompressed raw audio (largest file size, highest quality)
- **aac**: Modern compressed format with good quality

### Speech Rate Adjustment

Control speaking speed:

- `speech_rate=0`: Normal speed (1.0x)
- `speech_rate=100`: 2x speed (fast)
- `speech_rate=-50`: 0.5x speed (slow)

## Common Usage Patterns

### Pattern 1: Quick Blog Post to Podcast

```python
blog_text = """
[Your blog post content here - can be long form]
"""

result = await generator.generate_podcast(
    input_text=blog_text,
    output_path="blog_podcast.mp3"
)
```

### Pattern 2: Research Paper Summary

```python
paper_summary = "Summarize the key findings of the latest AI research..."

result = await generator.generate_podcast(
    input_text=paper_summary,
    output_path="research_podcast.mp3",
    use_head_music=True  # Add opening music for professional touch
)
```

### Pattern 3: Educational Content

```python
lesson_topic = "Explain quantum computing concepts for beginners"

result = await generator.generate_podcast(
    input_text=lesson_topic,
    output_path="lesson.mp3",
    speech_rate=-20  # Slightly slower for educational content
)
```

## Error Handling

Common issues and solutions:

**Connection Errors:**
- Verify APP_ID and ACCESS_KEY are correct
- Check network connectivity
- Ensure firewall allows WebSocket connections

**Text Too Long:**
- The model truncates at 25,000 characters
- Split long content into multiple podcasts

**Audio Not Generated:**
- Check output path is writable
- Verify sufficient disk space
- Review error messages for specific issues

**Incomplete Generation:**
- Use retry_info to resume from last completed round
- Check logs for the task_id and last_finished_round_id

## Resource Usage

### scripts/generate_podcast.py

Complete WebSocket client implementation for Volcano Engine's Podcast API:
- Handles binary protocol communication
- Manages streaming audio reception
- Implements automatic retry logic
- Provides both CLI and programmatic interfaces

**Key features:**
- Async/await pattern for efficient I/O
- Progress tracking with emoji indicators
- Comprehensive error handling
- Flexible parameter configuration

### references/api_reference.md

Detailed API documentation including:
- Complete parameter specifications
- WebSocket protocol details
- Event type reference
- Error code explanations

Consult this file for:
- Advanced API usage
- Protocol-level debugging
- Custom implementation needs

## Requirements

**Python dependencies:**
```bash
pip install websockets
```

**Credentials:**
- Volcano Engine APP ID (obtain from console: https://console.volcengine.com/speech/service/10028)
- Volcano Engine Access Key

## Best Practices

1. **Input Text Quality**: Use clear, well-structured Chinese text for best results
2. **Length Optimization**: Aim for 500-3000 characters for optimal podcast length
3. **Format Selection**: Use MP3 for distribution, PCM for further processing
4. **Error Handling**: Always check the `success` field in results
5. **Resource Management**: Close connections properly to avoid quota issues

## Limitations

- Maximum text length: 25,000 characters (model truncates longer input)
- Language support: Primarily optimized for Chinese
- Concurrent requests: Subject to your account's quota limits
- Audio quality: Determined by model capabilities, not controllable via parameters
