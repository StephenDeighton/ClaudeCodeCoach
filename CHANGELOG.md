# Changelog

All notable changes to Claude Code Coach will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Fix page with actionable prompts for all 22 health check detectors
- Comprehensive fix prompts with step-by-step guidance and code examples
- Filter issues by severity (Critical, Warning, Info)
- Sort issues by severity or title
- One-click copy-to-clipboard for fix prompts
- App state management service for sharing scan results between pages
- AppleScript path handling improvements for save report functionality

### Changed
- Renamed "Health" tab to "Scan" for clarity
- Updated navigation to include new Fix tab
- Improved error handling in save report dialog

### Fixed
- AppleScript file save dialog path conversion issues on macOS
- Added proper fallback for Mac-style to POSIX path conversion

## [0.1.0] - 2026-01-09

### Added
- Initial release of Claude Code Coach
- Health scan feature with 22 built-in detectors
  - 4 Critical severity checks
  - 13 Warning severity checks
  - 5 Info severity checks
- Health score calculation (0-100)
- Export scan reports to text files
- Settings page with light/dark theme toggle
- Native macOS folder picker integration
- Three-tier architecture (pages → services → database)
- SQLite database foundation
- Project scanner for detecting Claude Code projects
- Health checker service with decorator-based detector registration

### Health Check Detectors
**Critical:**
- No .gitignore file
- Secrets exposed
- Bloated CLAUDE.md
- Too many MCP servers

**Warning:**
- Missing Skills directory
- No status.md
- Extended thinking not enabled
- No hooks configured
- Missing README.md
- No tests directory
- No custom commands
- No subagents directory
- Model not explicitly set
- Large files detected
- No architecture documentation
- No changelog
- No planning documents

**Info:**
- Missing .env.example
- No /commit command
- No /init command
- No GitHub Actions
- Git worktrees not configured

### Technical
- Built with Flet 0.28.3
- Python 3.12+
- macOS native UI patterns
- Singleton service pattern
- Decorator-based detector registration
- Theme system with centralized constants

## [0.0.1] - 2026-01-09

### Added
- Project initialization
- Basic project structure
- Bootstrap from MeXuS template

---

**Note**: This project uses [Semantic Versioning](https://semver.org/):
- **MAJOR** version for incompatible API changes
- **MINOR** version for new functionality in a backwards compatible manner
- **PATCH** version for backwards compatible bug fixes
