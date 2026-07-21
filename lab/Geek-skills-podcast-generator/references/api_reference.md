# Volcano Engine Podcast API Reference

## API Endpoint

**WebSocket URL:** `wss://openspeech.bytedance.com/api/v3/sami/podcasttts`

## Authentication Headers

| Header | Required | Description | Example Value |
|--------|----------|-------------|---------------|
| X-Api-App-Id | Yes | APP ID from Volcano Console | your-app-id |
| X-Api-Access-Key | Yes | Access Token from Console | your-access-key |
| X-Api-Resource-Id | Yes | Resource ID for podcast service | volc.bigmodel.podcaster |
| X-Api-App-Key | Yes | Fixed value | aGjiRDfUWi |
| X-Api-Request-Id | No | UUID for tracking | 67ee89ba-7050-4c04-a3d7... |

**Get credentials:** https://console.volcengine.com/speech/service/10028

## Request Parameters

### Core Parameters

| Field | Type | Required | Description | Default |
|-------|------|----------|-------------|---------|
| action | number | Yes | Generation type: 0=generate podcast | 0 |
| input_text | string | Yes | Podcast topic text (truncated at 25k chars) | — |
| input_id | string | No | Unique ID for this podcast request | auto-generated |
| scene | string | No | Podcast scenario for statistics | deep_research |

### Audio Configuration

| Field | Type | Required | Description | Default |
|-------|------|----------|-------------|---------|
| audio_config.format | string | No | Audio format: mp3/ogg_opus/pcm/aac | pcm |
| audio_config.sample_rate | number | No | Sample rate in Hz | 24000 |
| audio_config.speech_rate | number | No | Speed adjustment: -50 to 100 (100=2x) | 0 |
| use_head_music | boolean | No | Add opening music effect | false |

### Speaker Configuration

| Field | Type | Required | Description | Default |
|-------|------|----------|-------------|---------|
| speaker_info.random_order | boolean | No | Randomize speaker order | true |
| speaker_info.speakers | array | No | List of speaker voice IDs | [default pair] |

**Default speakers:**
- `zh_male_dayixiansheng_v2_saturn_bigtts` (male)
- `zh_female_mizaitongxue_v2_saturn_bigtts` (female)

### Retry Configuration (for resuming)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| retry_info.retry_task_id | string | No | Task ID from incomplete generation |
| retry_info.last_finished_round_id | number | No | Last successfully completed round |

## WebSocket Protocol

### Binary Protocol Structure

All messages use binary protocol with 4-byte header + payload.

**Header format:**

| Byte | Bits 7-4 | Bits 3-0 | Description |
|------|----------|----------|-------------|
| 0 | Protocol version | Header size (4x) | Always: 0x11 (v1, 4-byte) |
| 1 | Message type | Message flags | Varies by message |
| 2 | Serialization | Compression | JSON=0x10, Raw=0x00 |
| 3 | Reserved | Reserved | Always: 0x00 |

### Event Types

#### Session Events

| Code | Name | Direction | Description |
|------|------|-----------|-------------|
| 1 | StartSession | Client→Server | Start generation |
| 150 | SessionStarted | Server→Client | Generation started |
| 152 | SessionFinished | Server→Client | Generation completed |
| 2 | FinishConnection | Client→Server | Close connection |
| 52 | ConnectionFinished | Server→Client | Connection closed |

#### Podcast Data Events

| Code | Name | Direction | Description |
|------|------|-----------|-------------|
| 360 | PodcastSpeaker | Server→Client | Round started (metadata) |
| 361 | PodcastTTSResponse | Server→Client | Audio data chunk |
| 362 | PodcastTTSRoundEnd | Server→Client | Round completed |

### Message Flow

1. Client: StartSession (event 1) with parameters
2. Server: SessionStarted (event 150)
3. **Loop for each round:**
   - Server: PodcastSpeaker (360)
   - Server: PodcastTTSResponse (361) - multiple times
   - Server: PodcastTTSRoundEnd (362)
4. Server: SessionFinished (event 152)
5. Client: FinishConnection (event 2)
6. Server: ConnectionFinished (event 52)

## Request Examples

### Basic Generation

```json
{
  "input_id": "test_001",
  "input_text": "分析下当前的大模型发展",
  "action": 0,
  "audio_config": {
    "format": "mp3",
    "sample_rate": 24000,
    "speech_rate": 0
  }
}
```

### Resume Generation

```json
{
  "input_text": "分析下当前的大模型发展",
  "action": 0,
  "retry_info": {
    "retry_task_id": "previous-session-id",
    "last_finished_round_id": 5
  }
}
```

## Error Codes

| Code | Message | Description |
|------|---------|-------------|
| 20000000 | ok | Success |
| 45000000 | quota exceeded | Concurrent limit exceeded |
| 55000000 | server error | Generic server error |

## Best Practices

1. **Always close connections properly** - Send FinishConnection after SessionFinished
2. **Handle interruptions** - Save task_id and last_finished_round_id for resume
3. **Monitor quotas** - Avoid concurrent request limits
4. **Validate input** - Check text length ≤ 25k characters
5. **Log responses** - Save X-Tt-Logid for debugging
