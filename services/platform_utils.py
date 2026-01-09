"""
Platform-specific utilities for ClaudeCodeCoach
Abstracts Mac/Windows/Linux differences
"""

import platform
import subprocess
import os
from pathlib import Path

from services.config_manager import get_config_manager


def reveal_in_file_manager(path: str) -> bool:
    """Open file manager and select the file/folder"""
    try:
        if platform.system() == "Darwin":
            subprocess.Popen(["open", "-R", path])
        elif platform.system() == "Windows":
            subprocess.run(["explorer", "/select,", path])
        else:
            subprocess.run(["xdg-open", os.path.dirname(path)])
        return True
    except Exception as e:
        print(f"Error revealing file: {e}")
        return False


def open_file(path: str) -> bool:
    """Open file with default application"""
    try:
        if platform.system() == "Darwin":
            subprocess.Popen(["open", path])
        elif platform.system() == "Windows":
            os.startfile(path)
        else:
            subprocess.run(["xdg-open", path])
        return True
    except Exception as e:
        print(f"Error opening file: {e}")
        return False


def open_folder(path: str) -> bool:
    """Open folder in file manager"""
    try:
        if platform.system() == "Darwin":
            subprocess.Popen(["open", path])
        elif platform.system() == "Windows":
            subprocess.run(["explorer", path])
        else:
            subprocess.run(["xdg-open", path])
        return True
    except Exception as e:
        print(f"Error opening folder: {e}")
        return False


def get_app_data_dir() -> Path:
    """Get application data directory for the current platform"""
    if platform.system() == "Darwin":
        return Path.home() / "Library" / "Application Support" / "ClaudeCodeCoach"
    elif platform.system() == "Windows":
        return Path(os.environ.get("APPDATA", "")) / "ClaudeCodeCoach"
    else:
        return Path.home() / ".coach"


def is_packaged_app() -> bool:
    """Detect if running as a packaged Flet app (.app bundle on macOS)"""
    import sys
    # Check if running from within a macOS .app bundle
    if platform.system() == "Darwin":
        # Packaged apps have sys.executable inside the .app bundle
        # e.g., .../ClaudeCodeCoach.app/Contents/MacOS/ClaudeCodeCoach
        exe_path = Path(sys.executable)
        return exe_path.parts and any(p.endswith('.app') for p in exe_path.parts)
    # For Windows/Linux, check if frozen
    return getattr(sys, 'frozen', False)


def get_default_db_path() -> Path:
    """Get the database path from active profile in ConfigManager"""
    try:
        config = get_config_manager()
        db_path = config.get_current_db_path()
        return Path(db_path)
    except Exception as e:
        # Fallback to app data directory if config manager fails
        print(f"⚠️ ConfigManager error, using fallback: {e}")
        # IMPORTANT: In packaged apps, don't use __file__ for writable paths!
        if is_packaged_app():
            # Use app data directory for database
            return get_app_data_dir() / "coach.db"
        else:
            # Development mode - use project directory
            return Path(__file__).parent.parent / "coach.db"


def is_mac() -> bool:
    return platform.system() == "Darwin"


def is_windows() -> bool:
    return platform.system() == "Windows"


def is_linux() -> bool:
    return platform.system() == "Linux"
