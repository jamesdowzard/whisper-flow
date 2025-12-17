# Whisper Flow

Local voice dictation with AI editing - an open source alternative to [Wispr Flow](https://wisprflow.ai).

**100% offline transcription** using [faster-whisper](https://github.com/SYSTRAN/faster-whisper). Your voice never leaves your device.

## Features

- **Local Transcription**: Uses OpenAI's Whisper model running locally via faster-whisper
- **AI Text Editing**: Optional cleanup using Ollama (local) or cloud APIs (OpenAI/Anthropic)
- **System-wide Hotkey**: Works in any application
- **Hold-to-talk or Toggle**: Choose your preferred recording mode
- **Multiple Presets**: Default, Email, Commit message, Notes, Code
- **Menu Bar App**: Native macOS menu bar integration

## Installation

### Prerequisites

- Python 3.10+
- macOS (Windows support planned)
- [Ollama](https://ollama.ai) (optional, for local AI editing)

### Install from source

```bash
git clone https://github.com/jamesdowzard/whisper-flow.git
cd whisper-flow
pip install -e .
```

### First run

On first run, Whisper Flow will download the selected model (~150MB for base model).

## Usage

### GUI Mode (macOS)

```bash
whisper-flow
```

This starts the menu bar app. Click the microphone icon to access settings.

**Default hotkey**: `Cmd+Shift+Space` (hold to talk)

### CLI Mode

```bash
whisper-flow --cli
```

### Options

```bash
whisper-flow --model small          # Use small model (more accurate)
whisper-flow --mode toggle          # Push-to-toggle instead of hold-to-talk
whisper-flow --editor ollama        # Enable Ollama AI editing
whisper-flow --preset email         # Use email formatting preset
whisper-flow --list-devices         # List audio input devices
```

## Configuration

Settings are stored in:
- macOS: `~/Library/Application Support/WhisperFlow/config.json`
- Windows: `%LOCALAPPDATA%/WhisperFlow/config.json`
- Linux: `~/.config/whisper-flow/config.json`

### AI Editing Providers

| Provider | Type | Setup |
|----------|------|-------|
| None | Rule-based | No setup needed |
| Ollama | Local LLM | Install [Ollama](https://ollama.ai), run `ollama pull llama3.2:3b` |
| OpenAI | Cloud API | Set `OPENAI_API_KEY` environment variable |
| Anthropic | Cloud API | Set `ANTHROPIC_API_KEY` environment variable |

### Whisper Models

| Model | Size | Speed | Accuracy |
|-------|------|-------|----------|
| tiny | ~75MB | Fastest | Basic |
| base | ~150MB | Fast | Good |
| small | ~500MB | Medium | Better |
| medium | ~1.5GB | Slow | Great |
| large-v3 | ~3GB | Slowest | Best |

## How It Works

1. Press hotkey to start recording
2. Speak naturally
3. Release hotkey (or press again in toggle mode)
4. Audio is transcribed locally using Whisper
5. (Optional) AI cleans up the text
6. Text is typed at your cursor position

## Comparison with Wispr Flow

| Feature | Whisper Flow | Wispr Flow |
|---------|--------------|------------|
| Transcription | Local (Whisper) | Cloud |
| Privacy | 100% offline | Cloud servers |
| AI Editing | Local (Ollama) or Cloud | Cloud |
| Price | Free & Open Source | $12/month |
| Speed | Depends on hardware | Fast (cloud) |
| Offline | Yes | No |

## Troubleshooting

### Microphone not working

1. Grant microphone permission in System Settings → Privacy & Security → Microphone
2. Check available devices: `whisper-flow --list-devices`

### Hotkey not working

Grant accessibility permission in System Settings → Privacy & Security → Accessibility

### Model download slow

Models are downloaded from Hugging Face on first use. Consider using `tiny` or `base` for faster download.

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Lint
ruff check src/
```

## License

MIT License - see [LICENSE](LICENSE)

## Credits

- [faster-whisper](https://github.com/SYSTRAN/faster-whisper) - Fast Whisper implementation
- [OpenAI Whisper](https://github.com/openai/whisper) - Original Whisper model
- [rumps](https://github.com/jaredks/rumps) - macOS menu bar framework
