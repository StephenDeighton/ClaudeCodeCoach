# Claude Code Coach (C3)

## Project Overview
A Flet-based Mac app that scans Claude Code project configurations for health issues and provides a searchable knowledge base about CC best practices.

## Architecture
- Three-tier: pages (UI) → services (logic) → database (SQLite)
- Based on MeXuS patterns
- Mac-first, Windows planned

## Code Standards
- Python 3.12+
- Flet 0.28.3 for UI
- All UI uses theme.py components
- Services are singletons via get_* functions
- No business logic in pages

## File Conventions
- Pages: class with build() → ft.Control
- Services: module with get_service() singleton pattern
- Health checks: class with check(config) → Optional[Issue]

## Testing Requirements
**CRITICAL**: Before ANY commit that modifies pages or services:
1. Test app launches without errors (`./start.sh`)
2. Navigate to each tab to verify no startup errors
3. Test the feature end-to-end
4. See `.claude/skills/testing.md` for complete checklist

**Startup Script**: Always use `./start.sh` to launch C3 - it cleans cache and validates environment

## Git Workflow
- **TEST FIRST** - Always test app launch before committing
- Commit after each working feature
- Update status.md with dated entries
- Keep commits atomic and descriptive
