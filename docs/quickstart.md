# Quick Start

## Starting Whisper Flow

```bash
# Default: floating overlay mode
whisper-flow

# CLI mode (terminal output)
whisper-flow --cli

# Menu bar mode (macOS only)
whisper-flow --menubar
```

## Basic Usage

1. **Start the app** - Run `whisper-flow`
2. **Look for the mic button** - Floating on the right side of your screen
3. **Hold the hotkey** - Cmd+Shift+Space (Mac) or Ctrl+Shift+Space (Windows)
4. **Speak** - Talk naturally
5. **Release** - Text appears at your cursor

## Hotkey Modes

### Hold-to-Talk (Default)
- Hold the hotkey while speaking
- Release to transcribe and insert

### Toggle Mode
- Press once to start recording
- Press again to stop and transcribe

```bash
# Switch to toggle mode
whisper-flow --mode toggle
```

## Adding Custom Words

Teach Whisper Flow your vocabulary:

```bash
# Add a name
whisper-flow --add-word "john smith" "John Smith"

# Add a company name
whisper-flow --add-word "acme corp" "ACME Corporation"

# Add a technical term
whisper-flow --add-word "kubernetes" "Kubernetes"

# View all words
whisper-flow --list-dictionary
```

## Adding Snippets

Create text shortcuts:

```bash
# Email signature
whisper-flow --add-snippet "sig" "Best regards,
James"

# Meeting link
whisper-flow --add-snippet "zoom" "https://zoom.us/j/123456789"

# Code template
whisper-flow --add-snippet "pydef" "def function_name():
    pass"

# View all snippets
whisper-flow --list-snippets
```

## Voice Commands

Say these commands instead of typing:

| Command | Action |
|---------|--------|
| "Delete that" | Remove last transcribed text |
| "Scratch that" | Same as delete that |
| "New line" | Press Enter |
| "New paragraph" | Press Enter twice |
| "Undo" | Cmd+Z / Ctrl+Z |
| "Delete last word" | Delete previous word |
| "Delete last 3 words" | Delete previous 3 words |

## Enabling AI Editing

```bash
# Use local Ollama
whisper-flow --editor ollama

# Use OpenAI (requires API key)
export OPENAI_API_KEY="sk-..."
whisper-flow --editor openai

# Use Anthropic (requires API key)
export ANTHROPIC_API_KEY="sk-ant-..."
whisper-flow --editor anthropic

# Disable AI editing
whisper-flow --editor none
```

## AI Presets

```bash
# Default - general cleanup
whisper-flow --preset default

# Email - professional formatting
whisper-flow --preset email

# Code - code/comments formatting
whisper-flow --preset code

# Notes - bullet point style
whisper-flow --preset notes

# Commit - git commit message style
whisper-flow --preset commit
```
