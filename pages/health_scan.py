"""
Health Scan Page for Claude Code Coach
Scan Claude Code projects for health issues
"""

import flet as ft
import subprocess
from pathlib import Path
from theme import Colors, Spacing, Radius, Typography, section_header, divider
from services.project_scanner import get_project_scanner
from services.health_checker import get_health_checker
from health_checks.base import Severity


class HealthScanPage:
    def __init__(self, page: ft.Page):
        self.page = page
        self.selected_path = None
        self.health_report = None

        # UI components that need updating
        self.path_display = ft.Text(
            "No directory selected",
            size=Typography.BODY_SM,
            color=Colors.TEXT_DARK_MUTED,
            italic=True,
        )
        self.scan_button = ft.ElevatedButton(
            "Scan Project",
            icon=ft.Icons.SEARCH_ROUNDED,
            disabled=True,
            on_click=self._on_scan_click,
        )
        self.results_container = ft.Container()

    def _on_pick_directory(self, e):
        """
        Open native macOS folder picker using osascript.

        PLATFORM-SPECIFIC CODE - macOS ONLY
        ====================================
        This is a workaround for Flet 0.28.3 FilePicker bug on macOS where
        ft.FilePicker().get_directory_path() fails silently with no dialog appearing.

        Related Issues:
        - https://github.com/flet-dev/flet/issues/5886 (fixed in Flet 0.8x+)
        - See: MeXuS KNOWN_FLET_ISSUES.md - Issue #1

        Migration Required:
        -------------------
        When upgrading to Flet 0.8x+ or 1.0 stable:
        Replace with: result = await ft.FilePicker().get_directory_path(...)

        Code Location: pages/health_scan.py:_on_pick_directory
        """
        try:
            # WORKAROUND: Use AppleScript to open native macOS folder picker
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
                # Successfully got a directory path
                path_str = result.stdout.strip()
                self.selected_path = Path(path_str)
                is_dark = self.page.theme_mode == ft.ThemeMode.DARK

                self.path_display.value = str(self.selected_path)
                self.path_display.italic = False
                self.path_display.color = Colors.TEXT_DARK if not is_dark else Colors.TEXT_LIGHT
                self.scan_button.disabled = False

                # Clear previous results
                self.results_container.content = None
                self.health_report = None

                self.page.update()
            # returncode 128 = user cancelled, don't show error

        except subprocess.TimeoutExpired:
            print("Folder picker timed out")
        except Exception as ex:
            print(f"Failed to open folder picker: {str(ex)}")

    def _on_scan_click(self, e):
        """Handle scan button click"""
        if not self.selected_path:
            return

        is_dark = self.page.theme_mode == ft.ThemeMode.DARK

        # Show loading state
        self.results_container.content = ft.Container(
            content=ft.Column(
                [
                    ft.ProgressRing(),
                    ft.Text(
                        "Scanning project...",
                        size=Typography.BODY_MD,
                        color=Colors.TEXT_DARK_MUTED if not is_dark else Colors.TEXT_LIGHT_MUTED,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=Spacing.MD,
            ),
            padding=Spacing.XL,
            alignment=ft.alignment.center,
        )
        self.page.update()

        # Run the scan
        scanner = get_project_scanner()
        project_info = scanner.scan_directory(self.selected_path)

        if not project_info:
            # Not a Claude Code project
            self.results_container.content = self._build_not_claude_project()
        else:
            # Run health checks
            checker = get_health_checker()
            self.health_report = checker.check_project(
                project_info.path,
                project_info.parsed_config
            )
            self.results_container.content = self._build_results()

        self.page.update()

    def _build_not_claude_project(self):
        """Build UI for non-Claude Code project"""
        is_dark = self.page.theme_mode == ft.ThemeMode.DARK

        return ft.Container(
            content=ft.Column(
                [
                    ft.Icon(
                        ft.Icons.FOLDER_OFF_ROUNDED,
                        size=64,
                        color=Colors.TEXT_DARK_MUTED if not is_dark else Colors.TEXT_LIGHT_MUTED,
                    ),
                    ft.Text(
                        "Not a Claude Code Project",
                        size=Typography.H2,
                        weight=ft.FontWeight.BOLD,
                        color=Colors.TEXT_DARK if not is_dark else Colors.TEXT_LIGHT,
                    ),
                    ft.Text(
                        "This directory doesn't appear to be a Claude Code project.\n"
                        "Claude Code projects should have a .claude/ directory or CLAUDE.md file.",
                        size=Typography.BODY_MD,
                        color=Colors.TEXT_DARK_MUTED if not is_dark else Colors.TEXT_LIGHT_MUTED,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=Spacing.MD,
            ),
            padding=Spacing.XL,
            alignment=ft.alignment.center,
        )

    def _build_results(self):
        """Build health scan results UI"""
        if not self.health_report:
            return None

        is_dark = self.page.theme_mode == ft.ThemeMode.DARK
        checker = get_health_checker()

        # Score indicator color
        score_color = checker.get_score_color(self.health_report.score)
        score_label = checker.get_score_label(self.health_report.score)

        # Map color names to actual colors
        color_map = {
            "green": Colors.GREEN_500,
            "yellow": Colors.YELLOW_500,
            "orange": Colors.ORANGE_500,
            "red": Colors.RED_500,
        }
        indicator_color = color_map.get(score_color, Colors.ACCENT_500)

        # Build issue cards
        issue_cards = []

        # Group issues by severity
        critical_issues = [i for i in self.health_report.issues if i.severity == Severity.CRITICAL]
        warning_issues = [i for i in self.health_report.issues if i.severity == Severity.WARNING]
        info_issues = [i for i in self.health_report.issues if i.severity == Severity.INFO]

        for issues, severity, emoji, color in [
            (critical_issues, "CRITICAL", "🔴", Colors.RED_500),
            (warning_issues, "WARNING", "🟡", Colors.YELLOW_500),
            (info_issues, "INFO", "🔵", Colors.BLUE_500),
        ]:
            for issue in issues:
                issue_card = self._build_issue_card(issue, emoji, color, is_dark)
                issue_cards.append(issue_card)

        # Build the controls list properly
        controls = [
            # Score header
            ft.Container(
                content=ft.Row(
                    [
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text(
                                        str(self.health_report.score),
                                        size=48,
                                        weight=ft.FontWeight.BOLD,
                                        color=indicator_color,
                                    ),
                                    ft.Text(
                                        "/ 100",
                                        size=Typography.BODY_MD,
                                        color=Colors.TEXT_DARK_MUTED if not is_dark else Colors.TEXT_LIGHT_MUTED,
                                    ),
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=0,
                            ),
                        ),
                        ft.Container(width=Spacing.XL),
                        ft.Column(
                            [
                                ft.Text(
                                    "Health Score",
                                    size=Typography.CAPTION,
                                    weight=ft.FontWeight.BOLD,
                                    color=Colors.TEXT_DARK_MUTED if not is_dark else Colors.TEXT_LIGHT_MUTED,
                                ),
                                ft.Text(
                                    score_label,
                                    size=Typography.H2,
                                    weight=ft.FontWeight.BOLD,
                                    color=Colors.TEXT_DARK if not is_dark else Colors.TEXT_LIGHT,
                                ),
                                ft.Text(
                                    f"{len(self.health_report.issues)} issues found",
                                    size=Typography.BODY_SM,
                                    color=Colors.TEXT_DARK_MUTED if not is_dark else Colors.TEXT_LIGHT_MUTED,
                                ),
                            ],
                            spacing=Spacing.XS,
                            expand=True,
                        ),
                    ],
                    spacing=Spacing.MD,
                ),
                padding=Spacing.XL,
                bgcolor=ft.Colors.with_opacity(0.05, indicator_color),
                border=ft.border.all(2, indicator_color),
                border_radius=Radius.LG,
            ),
            ft.Container(height=Spacing.MD),
        ]

        # Add issues or "no issues" message
        if issue_cards:
            controls.extend(issue_cards)
        else:
            controls.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Icon(
                                ft.Icons.CHECK_CIRCLE_ROUNDED,
                                size=64,
                                color=Colors.GREEN_500,
                            ),
                            ft.Text(
                                "No Issues Found!",
                                size=Typography.H2,
                                weight=ft.FontWeight.BOLD,
                                color=Colors.TEXT_DARK if not is_dark else Colors.TEXT_LIGHT,
                            ),
                            ft.Text(
                                "Your Claude Code project looks healthy.",
                                size=Typography.BODY_MD,
                                color=Colors.TEXT_DARK_MUTED if not is_dark else Colors.TEXT_LIGHT_MUTED,
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=Spacing.MD,
                    ),
                    padding=Spacing.XL,
                    alignment=ft.alignment.center,
                )
            )

        # Results layout
        return ft.Container(
            content=ft.Column(
                controls,
                spacing=Spacing.SM,
                scroll=ft.ScrollMode.AUTO,
            ),
            expand=True,
            padding=Spacing.MD,
        )

    def _build_issue_card(self, issue, emoji: str, color: str, is_dark: bool):
        """Build a card for a single issue"""
        return ft.Container(
            content=ft.Column(
                [
                    # Header
                    ft.Row(
                        [
                            ft.Text(
                                emoji,
                                size=24,
                            ),
                            ft.Column(
                                [
                                    ft.Row(
                                        [
                                            ft.Text(
                                                issue.severity.value.upper(),
                                                size=Typography.CAPTION,
                                                weight=ft.FontWeight.BOLD,
                                                color=color,
                                            ),
                                            ft.Container(
                                                width=2,
                                                height=12,
                                                bgcolor=Colors.LIGHT_BORDER_STRONG if not is_dark else Colors.PRIMARY_500,
                                            ),
                                            ft.Text(
                                                issue.rule_id,
                                                size=Typography.CAPTION,
                                                color=Colors.TEXT_DARK_MUTED if not is_dark else Colors.TEXT_LIGHT_MUTED,
                                            ),
                                        ],
                                        spacing=Spacing.SM,
                                    ),
                                    ft.Text(
                                        issue.title,
                                        size=Typography.BODY_LG,
                                        weight=ft.FontWeight.BOLD,
                                        color=Colors.TEXT_DARK if not is_dark else Colors.TEXT_LIGHT,
                                    ),
                                ],
                                spacing=Spacing.XS,
                                expand=True,
                            ),
                        ],
                        spacing=Spacing.MD,
                    ),
                    ft.Container(height=Spacing.SM),
                    # Message
                    ft.Text(
                        issue.message,
                        size=Typography.BODY_MD,
                        color=Colors.TEXT_DARK if not is_dark else Colors.TEXT_LIGHT,
                    ),
                    ft.Container(height=Spacing.SM),
                    # Suggestion
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(
                                    "💡 Suggestion",
                                    size=Typography.BODY_SM,
                                    weight=ft.FontWeight.BOLD,
                                    color=Colors.TEXT_DARK if not is_dark else Colors.TEXT_LIGHT,
                                ),
                                ft.Text(
                                    issue.suggestion,
                                    size=Typography.BODY_SM,
                                    color=Colors.TEXT_DARK_MUTED if not is_dark else Colors.TEXT_LIGHT_MUTED,
                                ),
                            ],
                            spacing=Spacing.XS,
                        ),
                        padding=Spacing.MD,
                        bgcolor=ft.Colors.with_opacity(0.03, color),
                        border_radius=Radius.MD,
                        border=ft.border.all(1, ft.Colors.with_opacity(0.2, color)),
                    ),
                    # File path if available
                    *(
                        [
                            ft.Container(height=Spacing.XS),
                            ft.Row(
                                [
                                    ft.Icon(
                                        ft.Icons.DESCRIPTION_OUTLINED,
                                        size=16,
                                        color=Colors.TEXT_DARK_MUTED if not is_dark else Colors.TEXT_LIGHT_MUTED,
                                    ),
                                    ft.Text(
                                        str(issue.file_path),
                                        size=Typography.TINY,
                                        color=Colors.TEXT_DARK_MUTED if not is_dark else Colors.TEXT_LIGHT_MUTED,
                                    ),
                                ],
                                spacing=Spacing.XS,
                            ),
                        ]
                        if issue.file_path
                        else []
                    ),
                ],
                spacing=Spacing.XS,
            ),
            padding=Spacing.MD,
            border=ft.border.all(2, Colors.LIGHT_BORDER_STRONG if not is_dark else Colors.PRIMARY_500),
            border_radius=Radius.MD,
            bgcolor=ft.Colors.with_opacity(0.02, color) if not is_dark else ft.Colors.with_opacity(0.05, color),
        )

    def build(self) -> ft.Control:
        """Build health scan page"""
        is_dark = self.page.theme_mode == ft.ThemeMode.DARK

        # Main content
        content = ft.Container(
            content=ft.Column(
                [
                    # Header
                    section_header(
                        "Health Scan",
                        "Scan your Claude Code projects for issues",
                        ft.Icons.MEDICAL_SERVICES_ROUNDED,
                        Colors.ACCENT_500,
                        is_dark=is_dark,
                    ),
                    divider(is_dark=is_dark),
                    # Directory picker section
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Row(
                                    [
                                        ft.Container(
                                            width=4,
                                            height=20,
                                            bgcolor=Colors.ACCENT_500,
                                            border_radius=Radius.SM,
                                        ),
                                        ft.Text(
                                            "SELECT PROJECT",
                                            size=Typography.CAPTION,
                                            weight=ft.FontWeight.BOLD,
                                            color=Colors.TEXT_DARK_MUTED if not is_dark else Colors.TEXT_LIGHT_MUTED,
                                        ),
                                    ],
                                    spacing=Spacing.SM,
                                ),
                                ft.Container(height=Spacing.SM),
                                ft.Row(
                                    [
                                        ft.ElevatedButton(
                                            "Choose Directory",
                                            icon=ft.Icons.FOLDER_OPEN_ROUNDED,
                                            on_click=self._on_pick_directory,
                                        ),
                                        self.scan_button,
                                    ],
                                    spacing=Spacing.MD,
                                ),
                                ft.Container(height=Spacing.XS),
                                self.path_display,
                            ],
                            spacing=Spacing.SM,
                        ),
                        padding=Spacing.MD,
                    ),
                    ft.Container(height=Spacing.MD),
                    # Results area
                    self.results_container,
                ],
                spacing=0,
                scroll=ft.ScrollMode.AUTO,
                expand=True,
            ),
            expand=True,
        )

        return content
