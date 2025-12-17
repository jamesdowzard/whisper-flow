"""Global hotkey handling."""

import sys
import threading
from typing import Callable

from pynput import keyboard

from .config import HotkeyConfig


class HotkeyHandler:
    """Handles global hotkey detection."""

    def __init__(
        self,
        config: HotkeyConfig,
        on_activate: Callable[[], None],
        on_deactivate: Callable[[], None] | None = None,
    ):
        self.config = config
        self.on_activate = on_activate
        self.on_deactivate = on_deactivate

        self._listener: keyboard.Listener | None = None
        self._pressed_keys: set[str] = set()
        self._hotkey_active = False
        self._is_toggled = False  # For toggle mode

    def _normalize_key(self, key) -> str | None:
        """Normalize a key to a string representation."""
        try:
            # Regular character key
            if hasattr(key, "char") and key.char:
                return key.char.lower()

            # Special keys
            if hasattr(key, "name"):
                return key.name.lower()

            # Handle Key enum
            key_str = str(key).replace("Key.", "").lower()

            # Normalize modifier names
            if key_str in ("cmd", "cmd_l", "cmd_r"):
                return "cmd"
            if key_str in ("ctrl", "ctrl_l", "ctrl_r"):
                return "ctrl"
            if key_str in ("shift", "shift_l", "shift_r"):
                return "shift"
            if key_str in ("alt", "alt_l", "alt_r", "option"):
                return "alt"

            return key_str

        except Exception:
            return None

    def _is_hotkey_pressed(self) -> bool:
        """Check if the configured hotkey combination is pressed."""
        required = {
            self.config.modifier1.lower(),
            self.config.modifier2.lower(),
            self.config.key.lower(),
        }
        return required.issubset(self._pressed_keys)

    def _on_press(self, key) -> None:
        """Handle key press events."""
        key_str = self._normalize_key(key)
        if key_str:
            self._pressed_keys.add(key_str)

        if self._is_hotkey_pressed() and not self._hotkey_active:
            self._hotkey_active = True

            if self.config.mode == "toggle":
                # Toggle mode: press once to start, press again to stop
                self._is_toggled = not self._is_toggled
                if self._is_toggled:
                    threading.Thread(target=self.on_activate, daemon=True).start()
                elif self.on_deactivate:
                    threading.Thread(target=self.on_deactivate, daemon=True).start()
            else:
                # Hold mode: activate on press
                threading.Thread(target=self.on_activate, daemon=True).start()

    def _on_release(self, key) -> None:
        """Handle key release events."""
        key_str = self._normalize_key(key)
        if key_str:
            self._pressed_keys.discard(key_str)

        # In hold mode, deactivate when hotkey is released
        if self.config.mode == "hold" and self._hotkey_active:
            if not self._is_hotkey_pressed():
                self._hotkey_active = False
                if self.on_deactivate:
                    threading.Thread(target=self.on_deactivate, daemon=True).start()

        # Reset hotkey active flag when all keys released
        if not self._pressed_keys:
            self._hotkey_active = False

    def start(self) -> None:
        """Start listening for hotkeys."""
        if self._listener is not None:
            return

        self._listener = keyboard.Listener(on_press=self._on_press, on_release=self._on_release)
        self._listener.start()

        mod1 = "Cmd" if self.config.modifier1 == "cmd" else self.config.modifier1.title()
        mod2 = self.config.modifier2.title()
        key = self.config.key.title()
        mode = "hold" if self.config.mode == "hold" else "toggle"

        print(f"Hotkey active: {mod1}+{mod2}+{key} ({mode} mode)")

    def stop(self) -> None:
        """Stop listening for hotkeys."""
        if self._listener:
            self._listener.stop()
            self._listener = None
        self._pressed_keys.clear()
        self._hotkey_active = False
        self._is_toggled = False

    def is_running(self) -> bool:
        """Check if the listener is running."""
        return self._listener is not None and self._listener.is_alive()

    def update_config(self, config: HotkeyConfig) -> None:
        """Update hotkey configuration."""
        was_running = self.is_running()
        if was_running:
            self.stop()

        self.config = config

        if was_running:
            self.start()
