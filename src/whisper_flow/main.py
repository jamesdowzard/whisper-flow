"""Main entry point for Whisper Flow."""

import argparse
import sys

from .config import load_settings, save_settings


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Whisper Flow - Local voice dictation with AI editing"
    )
    parser.add_argument(
        "--cli",
        action="store_true",
        help="Run in CLI mode (no menu bar)",
    )
    parser.add_argument(
        "--list-devices",
        action="store_true",
        help="List available audio input devices",
    )
    parser.add_argument(
        "--model",
        choices=["tiny", "base", "small", "medium", "large-v3"],
        help="Whisper model size",
    )
    parser.add_argument(
        "--mode",
        choices=["hold", "toggle"],
        help="Recording mode (hold-to-talk or push-to-toggle)",
    )
    parser.add_argument(
        "--editor",
        choices=["none", "ollama", "openai", "anthropic"],
        help="AI editor provider",
    )
    parser.add_argument(
        "--preset",
        choices=["default", "email", "commit", "notes", "code"],
        help="AI editor preset",
    )

    args = parser.parse_args()

    # List devices and exit
    if args.list_devices:
        from .recorder import AudioRecorder

        devices = AudioRecorder.list_devices()
        print("Available audio input devices:")
        for device in devices:
            print(f"  [{device['index']}] {device['name']}")
            print(f"      Channels: {device['channels']}, Sample Rate: {device['sample_rate']}")
        return

    # Load and potentially update settings
    settings = load_settings()

    if args.model:
        settings.whisper.model_size = args.model
        save_settings(settings)

    if args.mode:
        settings.hotkey.mode = args.mode
        save_settings(settings)

    if args.editor:
        settings.ai_editor.provider = args.editor
        settings.ai_editor.enabled = args.editor != "none"
        save_settings(settings)

    if args.preset:
        settings.ai_editor.preset = args.preset
        save_settings(settings)

    # Run appropriate mode
    if args.cli:
        run_cli(settings)
    else:
        run_gui(settings)


def run_cli(settings) -> None:
    """Run in CLI mode without GUI."""
    from .editor import create_editor
    from .hotkey import HotkeyHandler
    from .recorder import AudioRecorder
    from .transcriber import Transcriber
    from .typer import TextTyper

    print("Whisper Flow - CLI Mode")
    print("=" * 40)

    # Initialize components
    recorder = AudioRecorder(settings.audio)
    transcriber = Transcriber(settings.whisper)
    editor = create_editor(
        settings.ai_editor,
        {
            "openai": settings.openai_api_key,
            "anthropic": settings.anthropic_api_key,
        },
    )
    typer = TextTyper()

    # Load model
    print("Loading Whisper model...")
    transcriber.load_model()

    is_recording = False
    is_processing = False

    def on_activate():
        nonlocal is_recording
        if is_processing:
            return
        is_recording = True
        print("\n🔴 Recording...")
        recorder.start()

    def on_deactivate():
        nonlocal is_recording, is_processing
        if not is_recording:
            return

        is_recording = False
        is_processing = True
        print("⏳ Processing...")

        try:
            audio_data = recorder.stop()

            if not audio_data:
                print("No audio recorded")
                return

            text = transcriber.transcribe(audio_data)

            if not text:
                print("No speech detected")
                return

            print(f"📝 Transcribed: {text}")

            if settings.ai_editor.enabled:
                text = editor.edit(
                    text,
                    preset=settings.ai_editor.preset,
                    custom_prompt=settings.ai_editor.custom_prompt,
                )
                print(f"✨ Edited: {text}")

            typer.type_text(text)
            print("✅ Text inserted")

        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            is_processing = False

    # Set up hotkey handler
    hotkey = HotkeyHandler(
        settings.hotkey,
        on_activate=on_activate,
        on_deactivate=on_deactivate,
    )
    hotkey.start()

    mod1 = "Cmd" if settings.hotkey.modifier1 == "cmd" else settings.hotkey.modifier1.title()
    mod2 = settings.hotkey.modifier2.title()
    key = settings.hotkey.key.title()

    print(f"\nReady! Press {mod1}+{mod2}+{key} to record")
    print("Press Ctrl+C to quit\n")

    try:
        import time

        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nShutting down...")
        hotkey.stop()


def run_gui(settings) -> None:
    """Run with GUI (menu bar on macOS)."""
    if sys.platform == "darwin":
        from .ui.menubar import run_menubar_app

        run_menubar_app(settings)
    else:
        # Fall back to CLI mode on non-macOS
        print("GUI mode not available on this platform, running in CLI mode")
        run_cli(settings)


if __name__ == "__main__":
    main()
