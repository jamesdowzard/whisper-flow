#!/usr/bin/env python3
"""Launcher script for Rodin - handles both bundled and development modes."""

import sys
import os

# Add the src directory to path for development mode
if not getattr(sys, 'frozen', False):
    src_path = os.path.join(os.path.dirname(__file__), 'src')
    if os.path.exists(src_path):
        sys.path.insert(0, src_path)

# Now import and run
from rodin.main import main

if __name__ == '__main__':
    main()
