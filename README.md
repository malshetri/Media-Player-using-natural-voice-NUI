# Echo-Sync 🎵

**An inclusive, screen-free Natural User Interface media player for blind and motor-impaired users.**

*HTW Berlin — NUI Course — Group 7*

---

## What is Echo-Sync?

Echo-Sync is a voice-controlled media player that combines:

1. **Voice Control** — Direct commands: "play jazz," "pause," "next song," "volume up"
2. **AI Assistant** — Understands context: "I am exhausted" → plays calm music
3. **Guided Assistance** — Helps new users, handles errors, rejects off-topic requests
4. **Smart Ducking** — Automatically lowers music when speaking
5. **Earcon Feedback** — Audio cues for blind-accessible interaction

## Quick Start

### Prerequisites

- Python 3.11 or 3.12
- VLC media player installed
- OpenAI API key

### Setup

```bash
# Clone the repository
git clone <repo-url>
cd echo-sync

# Create virtual environment and install dependencies
pip install -e ".[dev]"

# Configure environment
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# Add music files to assets/music/{calm,energy,focus,happy,sad,fallback}/
```

### Run

```bash
# Voice mode (requires microphone)
python -m echo_sync.main

# Keyboard demo mode (type commands instead of speaking)
python -m echo_sync.main --demo-keyboard
```

### Run Tests

```bash
pytest tests/ -v
```

## Project Structure

```
echo-sync/
├── src/echo_sync/       # Main application code
│   ├── ai/              # AI intent classification
│   ├── audio/           # Microphone, earcons, ducking
│   ├── config/          # Settings and prompts
│   ├── interaction/     # Dialog management, guided help
│   ├── logging_utils/   # Interaction logging
│   ├── media/           # Music playback (VLC/Pygame)
│   └── speech/          # Speech-to-text
├── assets/              # Music and earcon files
├── docs/                # Project documentation
├── tests/               # Test suite
├── scripts/             # Helper scripts
└── logs/                # Interaction logs
```

## Three Modalities

| Modality | Description | Example |
|---|---|---|
| Direct Control | Immediate media commands | "Play jazz" → plays jazz |
| Context-Based | Mood/situation interpreted as music | "I am tired" → plays calm music |
| Guided Help | Assistance and error handling | Silence → "You can say: play jazz..." |

## Tech Stack

| Component | Technology |
|---|---|
| Language | Python 3.11+ |
| Speech-to-Text | OpenAI gpt-4o-mini-transcribe |
| AI Classification | OpenAI gpt-4o-mini |
| Music Playback | python-vlc / pygame |
| Audio Capture | sounddevice + soundfile |
| Audio Feedback | simpleaudio |
| Configuration | pydantic-settings |

## License

MIT License — see [LICENSE](LICENSE) for details.
