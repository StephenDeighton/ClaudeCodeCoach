"""
Version Management for Claude Code Coach
=============================

Provides version information for the application.
Version is auto-incremented on each build.
"""

import json
from pathlib import Path
from datetime import datetime
import sys


def _get_version_file_path() -> Path:
    """Get path to version.json file (handles both dev and packaged apps)"""
    import platform

    # Check if running as packaged app
    is_packaged = False
    if platform.system() == "Darwin":
        exe_path = Path(sys.executable)
        is_packaged = exe_path.parts and any(p.endswith('.app') for p in exe_path.parts)
    else:
        is_packaged = getattr(sys, 'frozen', False)

    if is_packaged:
        # Packaged app - version.json is in bundled assets
        if platform.system() == "Darwin":
            # Navigate from executable to assets directory in bundle
            exe_path = Path(sys.executable)
            # Find the .app directory
            app_path = None
            for i, part in enumerate(exe_path.parts):
                if part.endswith('.app'):
                    app_path = Path(*exe_path.parts[:i+1])
                    break
            if app_path:
                version_path = app_path / "Contents" / "Resources" / "flutter_assets" / "assets" / "version.json"
                if version_path.exists():
                    return version_path
        # Fallback for other platforms
        version_path = Path(sys.executable).parent / "assets" / "version.json"
        if version_path.exists():
            return version_path

    # Development mode - look in project root
    project_root = Path(__file__).parent.parent
    return project_root / "version.json"


def get_version_info() -> dict:
    """
    Get version information

    Returns:
        dict with keys: version, build_number, build_date, build_time
    """
    try:
        version_file = _get_version_file_path()
        if version_file.exists():
            with open(version_file, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"⚠️ Error reading version file: {e}")

    # Fallback version info
    return {
        "version": "1.0.0-alpha",
        "build_number": 0,
        "build_date": "Unknown",
        "build_time": "Unknown"
    }


def get_version_string() -> str:
    """
    Get formatted version string

    Returns:
        String like "Claude Code Coach v1.0.0-alpha (Build 42)"
    """
    info = get_version_info()
    return f"Claude Code Coach v{info['version']} (Build {info['build_number']})"


def get_version_with_date() -> str:
    """
    Get formatted version string with build date

    Returns:
        String like "Claude Code Coach v1.0.0-alpha (Build 42 - 2026-01-04 22:30)"
    """
    info = get_version_info()
    return f"Claude Code Coach v{info['version']} (Build {info['build_number']} - {info['build_date']} {info['build_time']})"


def increment_build_number():
    """
    Increment build number and update timestamp (UTC)

    Call this before building/packaging the app.
    Only works in development mode (not in packaged apps).
    """
    version_file = Path(__file__).parent.parent / "version.json"

    if not version_file.exists():
        print("⚠️ version.json not found")
        return

    try:
        # Read current version
        with open(version_file, 'r') as f:
            version_data = json.load(f)

        # Increment build number
        version_data['build_number'] = version_data.get('build_number', 0) + 1

        # Update timestamp (UTC)
        from datetime import timezone
        now = datetime.now(timezone.utc)
        version_data['build_date'] = now.strftime('%Y-%m-%d')
        version_data['build_time'] = now.strftime('%H:%M:%S') + ' UTC'

        # Write back
        with open(version_file, 'w') as f:
            json.dump(version_data, f, indent=2)

        print(f"✓ Version updated to build #{version_data['build_number']}")
        print(f"  Date: {version_data['build_date']} {version_data['build_time']}")

    except Exception as e:
        print(f"❌ Error updating version: {e}")


if __name__ == "__main__":
    # When run directly, increment the build number
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "increment":
        increment_build_number()
    else:
        # Just display current version
        print(get_version_with_date())
