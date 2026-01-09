# Claude Code Coach (C3) Architecture

## System Overview

Claude Code Coach is a desktop application that analyzes Claude Code project configurations for health issues and provides actionable fix prompts. Built with Python and Flet, it delivers a native macOS experience with plans for Windows support. The app scans projects, identifies configuration problems, and generates Claude-ready prompts to resolve them.

## Architecture Pattern: Three-Tier Layered Architecture

C3 follows a strict **three-tier layered architecture** inspired by the MeXuS pattern:

```
┌─────────────────────────────────────────────────┐
│         PRESENTATION LAYER (pages/)              │
│  - UI components and user interactions          │
│  - NO business logic                            │
│  - Flet controls and layouts                    │
└──────────────────┬──────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────┐
│         BUSINESS LAYER (services/)               │
│  - Core application logic                       │
│  - State management                             │
│  - Health check orchestration                   │
│  - Singleton pattern via get_*() functions      │
└──────────────────┬──────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────┐
│         DATA LAYER (database/)                   │
│  - SQLite persistence                           │
│  - Data models                                  │
│  - Future: Project history, settings storage    │
└─────────────────────────────────────────────────┘

         ┌────────────────────────────┐
         │  DETECTORS (health_checks/) │
         │  - Pluggable health checks  │
         │  - @register decorator      │
         │  - Critical/Warning/Info    │
         └────────────────────────────┘
```

### Why This Pattern?

- **Separation of Concerns**: UI, logic, and data are completely isolated
- **Testability**: Each layer can be tested independently
- **Maintainability**: Changes in one layer don't cascade to others
- **Scalability**: Easy to add new pages, services, or detectors
- **Claude-Friendly**: Clear structure helps Claude understand where to make changes

## Tech Stack

### Core Framework
- **Python 3.12+**: Modern Python with type hints
- **Flet 0.28.3**: Cross-platform UI framework (Flutter-based)
  - Enables native desktop apps from Python code
  - Reactive UI updates
  - Material Design components

### Storage
- **SQLite**: Embedded database (via `database/`)
  - Currently foundational, ready for expansion
  - Will store project history, scan results, user settings

### macOS Integration
- **AppleScript**: Native file dialogs and folder pickers
  - Custom path conversion handling (Mac-style → POSIX)
  - Fallback to Python path conversion when needed

### Development Tools
- **Git**: Version control with atomic commits
- **pytest**: Testing framework (being set up)
- **GitHub Actions**: CI/CD automation (being set up)

## Key Design Decisions

### 1. Three-Tier Architecture
**Decision**: Strict separation between pages, services, and database.

**Why**:
- Pages become thin UI layers that just render data
- Services contain all business logic, making them reusable
- Database layer can evolve without affecting UI

**Trade-offs**:
- More initial boilerplate
- ✅ But: Much easier to maintain and test long-term

### 2. Singleton Services
**Decision**: All services use `get_service()` pattern for singleton instances.

**Example**:
```python
# services/app_state.py
_state = AppState()

def get_state() -> AppState:
    return _state
```

**Why**:
- Single source of truth for shared state
- No prop drilling through UI components
- Easy to access from any layer

### 3. Decorator-Based Health Detectors
**Decision**: Health checks register via `@register` decorator.

**Example**:
```python
@register
class NoGitignoreDetector(BaseDetector):
    rule_id = "no-gitignore"
    severity = Severity.CRITICAL
    # ...
```

**Why**:
- Automatic discovery—no manual registration
- Easy to add new detectors (just create file + decorator)
- Clean separation: each detector is self-contained

**Alternatives Rejected**:
- Manual registration list (error-prone, easy to forget)
- Config file (adds complexity)

### 4. Fix Prompts as First-Class Data
**Decision**: Each health issue includes a `fix_prompt` field with step-by-step Claude instructions.

**Why**:
- Transforms C3 from reactive (shows problems) to proactive (provides solutions)
- Users can copy-paste directly into Claude Code
- Batch export enables fixing multiple issues at once

### 5. macOS-First Development
**Decision**: Build for macOS first, Windows later.

**Why**:
- Faster initial development targeting single platform
- Native OS integration (AppleScript) provides better UX
- Flet makes cross-platform port straightforward later

**Trade-offs**:
- Some macOS-specific code (AppleScript) will need Windows equivalents
- ✅ But: Core logic remains platform-agnostic

## Module Organization

```
ClaudeCodeCoach/
├── main.py                   # App entry point, navigation
├── theme.py                  # Centralized design system
│
├── pages/                    # PRESENTATION LAYER
│   ├── health_scan.py        # Scan tab: run health checks
│   ├── fix_page.py           # Fix tab: display issues with prompts
│   └── settings_page.py      # Settings tab: theme toggle
│
├── services/                 # BUSINESS LAYER
│   ├── app_state.py          # Shared state (scan results)
│   ├── project_scanner.py    # Detect Claude Code projects
│   └── health_checker.py     # Orchestrate health checks
│
├── health_checks/            # PLUGGABLE DETECTORS
│   ├── base.py               # BaseDetector, Severity, HealthIssue
│   ├── registry.py           # @register decorator, detector discovery
│   ├── critical/             # 4 critical severity checks
│   ├── warning/              # 13 warning severity checks
│   └── info/                 # 5 info severity checks
│
├── database/                 # DATA LAYER
│   └── db_service.py         # SQLite connection management
│
├── .claude/                  # Claude Code configuration
│   ├── CLAUDE.md             # Project instructions for Claude
│   ├── settings.json         # Permissions, hooks, model config
│   └── agents/               # Specialized subagents
│       └── code-reviewer.md  # Code review agent
│
├── tests/                    # TESTING
│   └── (being set up)
│
└── .github/workflows/        # CI/CD
    └── (being set up)
```

### Naming Conventions
- **Pages**: `*_page.py` with class ending in `Page`
- **Services**: `*_service.py` or descriptive name, singleton via `get_*()`
- **Detectors**: `*_detector.py` with class ending in `Detector`
- **Tests**: `test_*.py` matching source file structure

## Data Flow

### Health Scan Flow
```
User clicks "Select Project"
  ↓
health_scan.py (UI) → AppleScript folder picker
  ↓
project_scanner.py (service) → detect if Claude Code project
  ↓
health_checker.py (service) → discover & run all detectors
  ↓
health_checks/*/[detectors] → return HealthIssue objects
  ↓
app_state.py (service) → store ScanResult
  ↓
health_scan.py (UI) → display score + issue summary
```

### Fix Workflow
```
User navigates to Fix tab
  ↓
fix_page.py → app_state.get_last_scan()
  ↓
Display filtered/sorted issues
  ↓
User selects issues + clicks "Export Selected"
  ↓
fix_page.py → build batch export text
  ↓
Copy to clipboard
  ↓
User pastes into Claude Code CLI
  ↓
Claude fixes all issues systematically
```

### State Management
- **App State**: Singleton service (`app_state.py`) holds current scan results
- **UI State**: Each page manages its own local UI state (filters, sort order, selections)
- **No prop drilling**: Pages fetch shared state directly via `get_last_scan()`

### Request/Response Lifecycle
1. User interaction triggers event handler in page
2. Page calls service function (never contains business logic itself)
3. Service performs work, updates state if needed
4. Service returns result to page
5. Page updates UI controls
6. Page calls `page.update()` to trigger Flet re-render

## Component Interactions

### Health Check Detector Protocol
```python
class BaseDetector:
    rule_id: str
    severity: Severity
    title: str
    fix_prompt: Optional[str]

    def check(self, project_path: Path, config: dict) -> Optional[HealthIssue]:
        """Return HealthIssue if problem detected, None otherwise."""
        pass
```

All detectors:
1. Inherit from `BaseDetector`
2. Use `@register` decorator for auto-discovery
3. Implement `check()` method
4. Return `HealthIssue` or `None`

### Service Pattern
```python
# Singleton instance
_service = None

def get_service() -> ServiceClass:
    """Get or create singleton service instance."""
    global _service
    if _service is None:
        _service = ServiceClass()
    return _service
```

### Page Pattern
```python
class MyPage:
    def __init__(self, page: ft.Page):
        self.page = page
        # Initialize state

    def build(self) -> ft.Control:
        """Build and return the page UI."""
        return ft.Container(...)
```

## Future Architecture Considerations

### Planned Enhancements
- **Database Expansion**: Store scan history, track improvements over time
- **Settings Persistence**: Save user preferences to database
- **Windows Support**: Platform-agnostic file dialogs
- **Plugin System**: External detectors loaded at runtime
- **API Layer**: RESTful API for remote scanning

### Scalability Notes
- Current architecture easily supports 100+ detectors
- Decorator pattern makes detector addition O(1) complexity
- Three-tier separation allows independent scaling of each layer
- Flet framework supports both desktop and web deployment

## Development Guidelines

### Adding a New Page
1. Create `pages/new_page.py`
2. Define class with `__init__(self, page: ft.Page)` and `build() → ft.Control`
3. Use components from `theme.py`
4. NO business logic—call services only
5. Update `main.py` to add to navigation

### Adding a New Service
1. Create `services/new_service.py`
2. Define service class
3. Implement `get_new_service()` singleton function
4. Service contains business logic, no UI code
5. Import and use in pages

### Adding a New Health Detector
1. Create file in `health_checks/[critical|warning|info]/`
2. Import `BaseDetector`, `@register`, `HealthIssue`
3. Define detector class with `rule_id`, `severity`, `title`, `fix_prompt`
4. Implement `check()` method
5. Add `@register` decorator
6. That's it—auto-discovered!

---

This architecture enables rapid development while maintaining clarity for both human developers and Claude Code.
