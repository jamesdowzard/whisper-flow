# CLI Reference

## Basic Commands

```bash
whisper-flow [OPTIONS]
```

## Mode Options

| Option | Description |
|--------|-------------|
| `--overlay` | Run with floating overlay button (default) |
| `--cli` | Run in CLI mode (terminal output) |
| `--menubar` | Run with menu bar app (macOS only) |

## Configuration Options

| Option | Values | Description |
|--------|--------|-------------|
| `--model` | tiny, base, small, medium, large-v3 | Whisper model size |
| `--mode` | hold, toggle | Recording mode |
| `--editor` | none, ollama, openai, anthropic | AI editor provider |
| `--preset` | default, email, commit, notes, code | AI editing preset |

## Testing & Debugging

| Option | Description |
|--------|-------------|
| `--list-devices` | List available audio input devices |
| `--test TEXT` | Test AI editor with given text |
| `--benchmark` | Run performance benchmark |
| `--record-test N` | Record for N seconds and transcribe |

## Dictionary Management

| Option | Description |
|--------|-------------|
| `--add-word SPOKEN CORRECTED` | Add word to dictionary |
| `--remove-word SPOKEN` | Remove word from dictionary |
| `--list-dictionary` | List all dictionary entries |

## Snippet Management

| Option | Description |
|--------|-------------|
| `--add-snippet TRIGGER EXPANSION` | Add a snippet |
| `--remove-snippet TRIGGER` | Remove a snippet |
| `--list-snippets` | List all snippets |

## Examples

### Basic Usage

```bash
# Start with overlay
whisper-flow

# Start in CLI mode
whisper-flow --cli

# Use a larger model
whisper-flow --model small

# Enable Ollama editing
whisper-flow --editor ollama --preset email
```

### Dictionary Operations

```bash
# Add your name
whisper-flow --add-word "james dowzard" "James Dowzard"

# Add company name
whisper-flow --add-word "jhg" "John Holland Group"

# View dictionary
whisper-flow --list-dictionary

# Remove entry
whisper-flow --remove-word "jhg"
```

### Snippet Operations

```bash
# Add email signature
whisper-flow --add-snippet "sig" "Best regards,
James Dowzard
Senior Developer"

# Add meeting template
whisper-flow --add-snippet "standup" "Yesterday:
-

Today:
-

Blockers:
- None"

# View snippets
whisper-flow --list-snippets

# Remove snippet
whisper-flow --remove-snippet "sig"
```

### Testing

```bash
# List audio devices to find microphone
whisper-flow --list-devices

# Test 5-second recording
whisper-flow --record-test 5

# Test AI editor
whisper-flow --test "um like I was thinking we should uh update the code"

# Run benchmark
whisper-flow --benchmark
```

### Configuration via CLI

```bash
# Change model (persisted to config)
whisper-flow --model medium

# Change mode (persisted)
whisper-flow --mode toggle

# Change editor (persisted)
whisper-flow --editor ollama

# Change preset (persisted)
whisper-flow --preset email
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Error (see stderr for details) |
