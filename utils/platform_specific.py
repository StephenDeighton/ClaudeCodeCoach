"""
Platform-Specific Utilities
macOS AppleScript integration for file/folder dialogs

PLATFORM-SPECIFIC CODE - macOS ONLY
====================================
Workaround for Flet 0.28.3 FilePicker bugs on macOS.

Related Issues:
- https://github.com/flet-dev/flet/issues/5886 (fixed in Flet 0.8x+)

Migration Required:
-------------------
When upgrading to Flet 0.8x+ or 1.0 stable:
Replace with native Flet FilePicker API
"""

import subprocess
from pathlib import Path
from typing import Optional


def mac_path_to_posix(mac_path: str) -> str:
    """
    Convert Mac-style path (with colons) to POSIX path (with slashes).

    Args:
        mac_path: Mac-style path like "Macintosh HD:Users:name:file.txt"

    Returns:
        POSIX path like "/Users/name/file.txt"

    Example:
        >>> mac_path_to_posix("Macintosh HD:Users:name:file.txt")
        "/Users/name/file.txt"
    """
    # Remove leading "Macintosh HD:" and convert colons to slashes
    if mac_path.startswith("Macintosh HD:"):
        mac_path = mac_path[len("Macintosh HD:"):]

    # Replace colons with slashes
    posix_path = "/" + mac_path.replace(":", "/")
    return posix_path


def pick_folder() -> Optional[Path]:
    """
    Open native macOS folder picker dialog.

    Returns:
        Path object if folder selected, None if cancelled or error

    Raises:
        subprocess.TimeoutExpired: If dialog times out (5 minutes)
    """
    try:
        script = '''
        tell application "System Events"
            activate
            set theFolder to choose folder with prompt "Select Claude Code project directory"
            return POSIX path of theFolder
        end tell
        '''

        result = subprocess.run(
            ['osascript', '-e', script],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )

        if result.returncode == 0 and result.stdout.strip():
            path_str = result.stdout.strip()
            return Path(path_str)

        # returncode 128 = user cancelled
        return None

    except subprocess.TimeoutExpired:
        print("Folder picker timed out")
        return None
    except Exception as ex:
        print(f"Failed to open folder picker: {str(ex)}")
        return None


def save_file_dialog(default_name: str) -> Optional[Path]:
    """
    Open native macOS file save dialog.

    Args:
        default_name: Default filename (e.g., "report_20261009.txt")

    Returns:
        Path object if file location chosen, None if cancelled or error

    Raises:
        subprocess.TimeoutExpired: If dialog times out (5 minutes)

    Note:
        Handles both POSIX and Mac-style path formats from AppleScript.
    """
    try:
        script = f'''
        try
            set theFile to choose file name with prompt "Save Health Report" default name "{default_name}"
            try
                set posixPath to POSIX path of theFile
                return "POSIX:" & posixPath
            on error
                -- If POSIX conversion fails, return Mac-style path
                return "MAC:" & (theFile as text)
            end try
        on error errMsg number errNum
            return "ERROR:" & errNum & ":" & errMsg
        end try
        '''

        print(f"Opening file save dialog with default name: {default_name}")

        result = subprocess.run(
            ['osascript', '-e', script],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )

        print(f"Dialog result - returncode: {result.returncode}")
        print(f"Dialog result - stdout: '{result.stdout}'")

        # Check if output indicates an error
        if result.stdout.strip().startswith("ERROR:"):
            error_parts = result.stdout.strip().split(":", 3)
            if len(error_parts) >= 3:
                error_num = error_parts[1]
                error_msg = error_parts[2] if len(error_parts) >= 3 else "Unknown error"
                print(f"AppleScript error {error_num}: {error_msg}")
            return None

        if result.returncode == 0 and result.stdout.strip():
            output = result.stdout.strip()

            # Validate the path
            if not output or output.startswith("ERROR:"):
                print("Invalid file path returned")
                return None

            # Handle different path formats
            if output.startswith("POSIX:"):
                file_path_str = output[6:]  # Remove "POSIX:" prefix
            elif output.startswith("MAC:"):
                mac_path = output[4:]  # Remove "MAC:" prefix
                file_path_str = mac_path_to_posix(mac_path)
                print(f"Converted Mac path to POSIX: {mac_path} -> {file_path_str}")
            else:
                # Assume it's already a POSIX path
                file_path_str = output

            return Path(file_path_str)

        # returncode 128 = user cancelled
        print(f"Dialog cancelled or failed - returncode: {result.returncode}")
        return None

    except subprocess.TimeoutExpired:
        print("File save dialog timed out")
        return None
    except Exception as ex:
        print(f"Failed to open save dialog: {str(ex)}")
        import traceback
        traceback.print_exc()
        return None
