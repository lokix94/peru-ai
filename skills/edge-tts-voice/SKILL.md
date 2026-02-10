---
name: edge-tts-voice
description: Generate speech audio from text using Microsoft Edge TTS (free, no API key). Use when the user asks for text-to-speech, voice messages, audio output, or spoken content. Supports 300+ voices across 100+ languages with natural-sounding neural speech.
---

# Edge TTS Voice

Generate natural speech from text using Microsoft Edge TTS — completely free, no API key needed.

## Installation

```bash
pip3 install edge-tts
```

## Quick Usage

```bash
# Generate audio
edge-tts --voice en-US-AriaNeural --text "Hello world" --write-media output.mp3

# List all available voices
edge-tts --list-voices

# Filter by language
edge-tts --list-voices | grep "es-"
```

## Generating Speech

```bash
bash scripts/speak.sh "Your text here" [voice] [output_file]
```

- **text** (required): Text to speak
- **voice** (optional): Voice ID (default: en-US-AriaNeural)
- **output** (optional): Output file path (default: /tmp/tts_output.mp3)

## Popular Voices

| Voice ID | Language | Gender | Accent |
|----------|----------|--------|--------|
| en-US-AriaNeural | English | Female | American |
| en-US-GuyNeural | English | Male | American |
| en-GB-SoniaNeural | English | Female | British |
| es-PE-CamilaNeural | Spanish | Female | Peruvian |
| es-PE-AlexNeural | Spanish | Male | Peruvian |
| es-MX-DaliaNeural | Spanish | Female | Mexican |
| fr-FR-DeniseNeural | French | Female | French |
| de-DE-KatjaNeural | German | Female | German |
| ja-JP-NanamiNeural | Japanese | Female | Japanese |
| zh-CN-XiaoxiaoNeural | Chinese | Female | Mandarin |
| pt-BR-FranciscaNeural | Portuguese | Female | Brazilian |

For full list: `edge-tts --list-voices`

## Tips

- **Max length**: No hard limit, but split texts >5000 chars for reliability
- **File format**: Output is MP3 by default
- **Speed/pitch**: Not adjustable via CLI, but voice selection gives variety
- **Telegram/Discord**: Send as voice message for inline playback
- **Concatenation**: Use `ffmpeg -i "concat:a.mp3|b.mp3" -c copy merged.mp3` for long texts
