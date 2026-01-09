"""
Configuration Manager for ClaudeCodeCoach
================================

Manages application configuration including database profiles.
Enables switching between production, test, and development databases.

Config file location: ~/.coach/config.json
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import sys

class ConfigManager:
    """Manage application configuration and database profiles"""

    def __init__(self):
        # Config directory in user's home
        self.config_dir = Path.home() / ".coach"
        self.config_file = self.config_dir / "config.json"

        # Default database directory
        # IMPORTANT: In packaged apps, don't use __file__ for writable paths!
        self.project_root = self._get_project_root()

        # Ensure config exists
        self._ensure_config_exists()

    def _get_project_root(self) -> Path:
        """Get project root directory (handles both dev and packaged apps)"""
        # Check if running as packaged app
        is_packaged = self._is_packaged_app()

        if is_packaged:
            # Packaged app - use app data directory for writable files
            # ~/Library/Application Support/ClaudeCodeCoach on macOS
            import platform
            if platform.system() == "Darwin":
                return Path.home() / "Library" / "Application Support" / "ClaudeCodeCoach"
            elif platform.system() == "Windows":
                import os
                return Path(os.environ.get("APPDATA", "")) / "ClaudeCodeCoach"
            else:
                return Path.home() / ".coach"
        else:
            # Development mode - use actual project directory
            return Path(__file__).parent.parent

    def _is_packaged_app(self) -> bool:
        """Detect if running as a packaged Flet app"""
        import platform
        # Check if frozen (PyInstaller/similar)
        if getattr(sys, 'frozen', False):
            return True

        # Check if running from within OUR .app bundle (not Xcode.app or other apps)
        if platform.system() == "Darwin":
            exe_path = Path(sys.executable)
            # Only consider it packaged if it's specifically in ClaudeCodeCoach.app
            return any(p == 'ClaudeCodeCoach.app' for p in exe_path.parts)

        return False

    def _ensure_config_exists(self):
        """Create config directory and default config if not exists"""
        # Create directory
        self.config_dir.mkdir(parents=True, exist_ok=True)

        # Create default config if doesn't exist
        if not self.config_file.exists():
            # Create default production profile automatically
            default_db_path = str(self.project_root / "coach.db")

            default_config = {
                "version": "1.0",
                "current_profile": "production",  # Auto-select production profile
                "profiles": {
                    "production": {
                        "name": "Production Database",
                        "db_path": default_db_path,
                        "description": "Main database with all knowledge topics",
                        "created": datetime.now().isoformat(),
                        "last_used": datetime.now().isoformat(),
                        "read_only": False
                    }
                },
                "app_settings": {
                    "check_for_updates": True,
                    "debug_mode": False
                }
            }
            self._save_config(default_config)
            print(f"✅ Created default production profile: {default_db_path}")

    def _load_config(self) -> dict:
        """Load configuration from file"""
        with open(self.config_file, 'r') as f:
            return json.load(f)

    def _save_config(self, config: dict):
        """Save configuration to file"""
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)

    def get_current_profile_name(self) -> Optional[str]:
        """Get name of currently active profile"""
        config = self._load_config()
        return config.get("current_profile")

    def get_current_db_path(self) -> Optional[str]:
        """Get database path for currently active profile"""
        config = self._load_config()
        current_profile = config.get("current_profile")

        if not current_profile:
            return None

        if current_profile not in config["profiles"]:
            print(f"⚠️ Profile '{current_profile}' not found")
            return None

        db_path = config["profiles"][current_profile]["db_path"]
        return db_path

    def get_profile(self, profile_name: str) -> Optional[Dict]:
        """Get profile information by name"""
        config = self._load_config()
        return config["profiles"].get(profile_name)

    def get_all_profiles(self) -> List[str]:
        """Get list of all profile names"""
        config = self._load_config()
        return list(config["profiles"].keys())

    def add_profile(self, profile_key: str, profile_data: Dict) -> bool:
        """
        Add a new profile

        Args:
            profile_key: Unique profile identifier (e.g., 'steves_work_emails')
            profile_data: Profile information dict with keys:
                - name: Display name
                - db_path: Database file path
                - description: Optional description
                - created: ISO timestamp
                - last_used: ISO timestamp
                - read_only: Boolean

        Returns:
            True if added successfully, False if profile already exists
        """
        config = self._load_config()

        if profile_key in config["profiles"]:
            print(f"❌ Profile '{profile_key}' already exists")
            return False

        config["profiles"][profile_key] = profile_data
        self._save_config(config)
        print(f"✅ Added profile: {profile_key}")
        return True

    def set_current_profile(self, profile_key: str) -> bool:
        """
        Set the current active profile

        Args:
            profile_key: Profile identifier to activate

        Returns:
            True if set successfully, False if profile doesn't exist
        """
        config = self._load_config()

        if profile_key not in config["profiles"]:
            print(f"❌ Profile '{profile_key}' not found")
            return False

        config["current_profile"] = profile_key

        # Update last_used timestamp
        config["profiles"][profile_key]["last_used"] = datetime.now().isoformat()

        self._save_config(config)
        print(f"✅ Set current profile to: {profile_key}")
        return True

    def list_profiles(self) -> List[Dict]:
        """Get all available profiles"""
        config = self._load_config()
        profiles = []

        for profile_id, info in config["profiles"].items():
            profile = {
                "profile_id": profile_id,  # The key (e.g., "production", "test_blank")
                **info
            }

            # Add file size if DB exists
            db_path = Path(info["db_path"])
            if db_path.exists():
                size_bytes = db_path.stat().st_size
                size_mb = size_bytes / (1024 * 1024)
                size_gb = size_bytes / (1024 * 1024 * 1024)

                if size_gb >= 1:
                    profile["size"] = f"{size_gb:.2f} GB"
                else:
                    profile["size"] = f"{size_mb:.1f} MB"
                profile["exists"] = True
            else:
                profile["size"] = "Not found"
                profile["exists"] = False

            profiles.append(profile)

        return profiles

    def create_profile(self, name: str, db_path: str, description: str = "") -> bool:
        """Create a new database profile"""
        config = self._load_config()

        # Check if profile already exists
        if name in config["profiles"]:
            print(f"❌ Profile '{name}' already exists")
            return False

        # Add new profile
        config["profiles"][name] = {
            "name": description or name,
            "db_path": db_path,
            "description": description,
            "created": datetime.now().isoformat()
        }

        self._save_config(config)
        print(f"✅ Created profile: {name}")
        return True

    def delete_profile(self, profile_name: str) -> bool:
        """Delete a profile (does not delete the database file)"""
        config = self._load_config()

        # Cannot delete production
        if profile_name == "production":
            print(f"❌ Cannot delete production profile")
            return False

        # Cannot delete current profile
        if profile_name == config["current_profile"]:
            print(f"❌ Cannot delete active profile. Switch to another profile first.")
            return False

        # Delete profile
        if profile_name in config["profiles"]:
            del config["profiles"][profile_name]
            self._save_config(config)
            print(f"✅ Deleted profile: {profile_name}")
            return True
        else:
            print(f"❌ Profile '{profile_name}' not found")
            return False

    def switch_profile(self, profile_name: str) -> bool:
        """Switch to a different database profile"""
        config = self._load_config()

        # Check if profile exists
        if profile_name not in config["profiles"]:
            print(f"❌ Profile '{profile_name}' not found")
            return False

        # Check if database file exists
        db_path = Path(config["profiles"][profile_name]["db_path"])
        if not db_path.exists():
            print(f"⚠️ Warning: Database file not found: {db_path}")
            print(f"   Profile will be set, but app may fail to start")

        # Update current profile
        old_profile = config["current_profile"]
        config["current_profile"] = profile_name
        self._save_config(config)

        print(f"✅ Switched from '{old_profile}' to '{profile_name}'")
        print(f"   ⚠️ IMPORTANT: Restart the app for changes to take effect!")
        return True

    def get_setting(self, key: str, default=None):
        """Get an application setting"""
        config = self._load_config()
        return config.get("app_settings", {}).get(key, default)

    def set_setting(self, key: str, value):
        """Set an application setting"""
        config = self._load_config()
        if "app_settings" not in config:
            config["app_settings"] = {}
        config["app_settings"][key] = value
        self._save_config(config)

    def get_debug_mode(self) -> bool:
        """Check if debug mode is enabled"""
        return self.get_setting("debug_mode", False)

    def set_debug_mode(self, enabled: bool):
        """Enable or disable debug mode"""
        self.set_setting("debug_mode", enabled)


# Global singleton instance
_config_manager = None

def get_config_manager() -> ConfigManager:
    """Get the global ConfigManager instance"""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager


if __name__ == "__main__":
    # Test the config manager
    print("=" * 70)
    print("ConfigManager Test")
    print("=" * 70)

    manager = ConfigManager()

    print(f"\n📁 Config file: {manager.config_file}")
    print(f"📁 Current profile: {manager.get_current_profile_name()}")
    print(f"💾 Current DB path: {manager.get_current_db_path()}")

    print(f"\n📋 Available profiles:")
    for profile in manager.list_profiles():
        active = "✓" if profile["name"] == manager.get_current_profile_name() else " "
        exists = "✓" if profile["exists"] else "✗"
        print(f"  [{active}] {profile['name']}: {profile.get('size', '?')} (exists: {exists})")
        print(f"      {profile['db_path']}")

    print("\n" + "=" * 70)
