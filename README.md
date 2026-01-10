# Claude Code Coach (C3)

A Mac desktop application for scanning Claude Code projects and providing actionable health recommendations with AI-powered fix prompts.

## Overview

Claude Code Coach helps developers maintain healthy Claude Code projects by:
- **Scanning** projects for 22 common configuration issues
- **Detecting** critical problems like exposed secrets, bloated configs, and missing documentation
- **Providing** actionable fix prompts that you can copy directly to Claude Code
- **Filtering** issues by severity (Critical, Warning, Info)

## Features

### 🔍 Health Scan
- Scans Claude Code projects for configuration issues
- Assigns health score (0-100) based on detected issues
- Identifies critical security issues, warnings, and suggestions
- Exports scan reports to text files

### 🔧 Fix Page
- Displays all detected issues with comprehensive fix prompts
- Filter by severity level
- Sort by severity or title
- One-click copy of fix prompts to paste into Claude Code
- Each prompt provides step-by-step guidance with code examples

### ⚙️ Settings
- Light/Dark theme toggle
- Persistent theme preference
- Clean, native macOS UI

## Installation

### Prerequisites
- Python 3.12+
- macOS (Windows support planned)
- Flet 0.28.3

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ClaudeCodeCoach
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv_312
   source venv_312/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   ./start.sh
   ```

   Or manually:
   ```bash
   python3 main.py
   ```

   The `start.sh` script ensures a clean start by:
   - Verifying Python 3.12+ is installed
   - Cleaning Python cache (`__pycache__`, `.pyc` files)
   - Checking all dependencies are installed
   - Launching the app with proper environment

## Usage

### Scanning a Project

1. Launch Claude Code Coach
2. Navigate to **Scan** tab
3. Click **Choose Directory** and select your Claude Code project
4. Click **Scan Project**
5. View health score and detected issues

### Getting Fix Recommendations

1. After scanning, navigate to **Fix** tab
2. Browse detected issues
3. Use filters to narrow down by severity
4. Click **Copy Prompt** on any issue
5. Paste the prompt into Claude Code for guided fixes

### Exporting Reports

1. After scanning, click **Save Report** button
2. Choose a location and filename
3. Report saves as plain text with all issue details

## Project Structure

```
ClaudeCodeCoach/
├── main.py                 # Application entry point
├── theme.py               # UI theme and reusable components
├── pages/                 # UI pages
│   ├── health_scan.py    # Scan page
│   ├── fix_page.py       # Fix recommendations page
│   └── settings.py       # Settings page
├── services/             # Business logic
│   ├── health_checker.py # Health check orchestration
│   ├── project_scanner.py # Claude project detection
│   └── app_state.py      # Shared state management
├── health_checks/        # Health check detectors
│   ├── critical/         # Critical severity checks
│   ├── warning/          # Warning severity checks
│   └── info/             # Info severity checks
├── data/                 # SQLite database (future)
└── .claude/              # Claude Code configuration
    ├── CLAUDE.md         # Project instructions
    ├── settings.json     # Project settings
    └── commands/         # Custom commands
```

## Architecture

### Three-Tier Pattern
- **Pages**: UI layer using Flet components
- **Services**: Business logic layer (singletons via `get_*()` functions)
- **Health Checks**: Detector modules using decorator pattern

### Key Design Patterns
- **Singleton Services**: All services use `get_service()` pattern
- **Decorator Pattern**: Health detectors register via `@register` decorator
- **State Management**: Shared state via `app_state` service
- **Theme System**: Centralized theme constants in `theme.py`

## Health Check Detectors

C3 includes 22 built-in health check detectors across three severity levels:

### Critical (4 checks)
- No .gitignore file
- Secrets exposed (unprotected .env or settings)
- Bloated CLAUDE.md (>50 lines)
- Too many MCP servers (>3)

### Warning (13 checks)
- Missing Skills directory
- No status.md tracking
- Extended thinking not enabled
- No hooks configured
- Missing README.md
- No tests directory
- No custom commands
- No subagents directory
- Model not explicitly set
- Large files (>400 lines)
- No architecture documentation
- No changelog
- No planning documents

### Info (5 checks)
- Missing .env.example template
- No /commit command
- No /init command
- No GitHub Actions
- Git worktrees not configured

## Development

### Adding New Detectors

1. Create detector file in appropriate severity directory
2. Inherit from `BaseDetector`
3. Implement `check()` method
4. Add `fix_prompt` class attribute
5. Decorate with `@register`

Example:
```python
from health_checks.base import BaseDetector, HealthIssue, Severity
from health_checks import register

@register
class MyDetector(BaseDetector):
    rule_id = "my-check"
    severity = Severity.WARNING
    title = "My Check Title"

    fix_prompt = \"\"\"Fix instructions here...\"\"\"

    def check(self, project_path: Path, config: dict) -> Optional[HealthIssue]:
        # Detection logic
        if issue_detected:
            return HealthIssue(
                rule_id=self.rule_id,
                severity=self.severity,
                title=self.title,
                message="Issue description",
                suggestion="What to do",
                fix_prompt=self.fix_prompt,
                topic_slug="kb-article"
            )
        return None
```

### Building for Distribution

```bash
# Build macOS app
./build_app.sh

# Output in dist/ directory
```

## Contributing

Contributions welcome! Please:
1. Follow existing code patterns
2. Add health check detectors for new issues
3. Include fix prompts with code examples
4. Test on macOS before submitting
5. Update CHANGELOG.md

## Roadmap

- [ ] Windows support
- [ ] Knowledge base integration
- [ ] Auto-fix capabilities
- [ ] Project templates
- [ ] Cloud backup/sync
- [ ] Team sharing features

## License

[Add your license here]

## Credits

Built with:
- [Flet](https://flet.dev/) - Python UI framework
- [Claude Sonnet 4.5](https://anthropic.com/) - AI assistance
- Based on MeXuS patterns

---

**Claude Code Coach** - Maintain healthy Claude Code projects with confidence.
