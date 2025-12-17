"""Text insertion at cursor position."""

import sys
import time

import pyperclip
from pynput.keyboard import Controller, Key


class TextTyper:
    """Inserts text at the current cursor position."""

    def __init__(self, typing_delay: float = 0.01):
        self.keyboard = Controller()
        self.typing_delay = typing_delay

    def type_text(self, text: str, method: str = "auto") -> None:
        """Type text at the current cursor position.

        Args:
            text: Text to type
            method: Insertion method - "type", "paste", or "auto"
        """
        if not text:
            return

        if method == "auto":
            # Use paste for longer text (faster), type for short text
            method = "paste" if len(text) > 50 else "type"

        if method == "paste":
            self._paste_text(text)
        else:
            self._type_text(text)

    def _type_text(self, text: str) -> None:
        """Type text character by character."""
        for char in text:
            self.keyboard.type(char)
            if self.typing_delay > 0:
                time.sleep(self.typing_delay)

    def _paste_text(self, text: str) -> None:
        """Paste text using clipboard."""
        # Save current clipboard content
        try:
            original_clipboard = pyperclip.paste()
        except Exception:
            original_clipboard = None

        try:
            # Copy text to clipboard
            pyperclip.copy(text)

            # Small delay to ensure clipboard is ready
            time.sleep(0.05)

            # Paste using keyboard shortcut
            modifier = Key.cmd if sys.platform == "darwin" else Key.ctrl
            with self.keyboard.pressed(modifier):
                self.keyboard.tap("v")

            # Small delay before restoring clipboard
            time.sleep(0.1)

        finally:
            # Restore original clipboard content
            if original_clipboard is not None:
                try:
                    pyperclip.copy(original_clipboard)
                except Exception:
                    pass

    def press_key(self, key: Key | str) -> None:
        """Press a single key."""
        if isinstance(key, str):
            self.keyboard.tap(key)
        else:
            self.keyboard.tap(key)

    def press_enter(self) -> None:
        """Press Enter key."""
        self.keyboard.tap(Key.enter)

    def press_tab(self) -> None:
        """Press Tab key."""
        self.keyboard.tap(Key.tab)
