"""
Health Scan Page for Claude Code Coach
Scan Claude Code projects for health issues
"""

import flet as ft
from datetime import datetime
from pathlib import Path
from theme import Colors, Spacing, Radius, Typography, section_header, divider
from services.project_scanner import get_project_scanner
from services.health_checker import get_health_checker
from services.app_state import set_last_scan, set_wizard_path, ScanResult
from services.tech_stack_analyzer import get_tech_stack_analyzer
from services.status_updater import get_status_updater
from health_checks.base import Severity
from utils.platform_specific import pick_folder, save_file_dialog
from utils.report_formatter import format_health_report
from pages.components.issue_card import build_issue_card
from pages.components.scan_results import build_scan_results, build_not_claude_project


class HealthScanPage:
    def __init__(self, page: ft.Page, on_navigate=None):
        self.page = page
        self.on_navigate = on_navigate
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
        """Open folder picker and update UI with selected path."""
        selected_folder = pick_folder()

        if selected_folder:
            self.selected_path = selected_folder
            is_dark = self.page.theme_mode == ft.ThemeMode.DARK

            self.path_display.value = str(self.selected_path)
            self.path_display.italic = False
            self.path_display.color = Colors.TEXT_DARK if not is_dark else Colors.TEXT_LIGHT
            self.scan_button.disabled = False

            # Clear previous results
            self.results_container.content = None
            self.health_report = None

            self.page.update()

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
            # No .claude/ found - check if it's a valid code project
            analyzer = get_tech_stack_analyzer()
            tech_info = analyzer.analyze_directory(self.selected_path)
            is_valid, reason = analyzer.is_valid_code_project(tech_info)

            if is_valid:
                # Valid code project without .claude - offer to set up CC
                self.results_container.content = self._build_setup_prompt()
            else:
                # Not a code project at all
                self.results_container.content = self._build_not_claude_project()
        else:
            # Run health checks
            checker = get_health_checker()
            self.health_report = checker.check_project(
                project_info.path,
                project_info.parsed_config
            )

            # Store scan results in app state for Fix page
            scan_result = ScanResult(
                project_path=project_info.path,
                scan_time=datetime.now(),
                score=self.health_report.score,
                issues=self.health_report.issues,
                detectors_run=self.health_report.detectors_run
            )
            set_last_scan(scan_result)

            # Update status.md with scan results
            updater = get_status_updater()
            updater.append_scan_result(
                project_info.path,
                self.health_report.score,
                len(self.health_report.issues)
            )

            self.results_container.content = self._build_results()

        self.page.update()

    def _build_not_claude_project(self):
        """Build UI for non-Claude Code project"""
        is_dark = self.page.theme_mode == ft.ThemeMode.DARK
        return build_not_claude_project(is_dark)

    def _build_results(self):
        """Build health scan results UI"""
        is_dark = self.page.theme_mode == ft.ThemeMode.DARK
        return build_scan_results(
            health_report=self.health_report,
            is_dark=is_dark,
            build_issue_card_fn=self._build_issue_card,
            on_save_report=self._on_save_report,
        )

    def _build_issue_card(self, issue, emoji: str, color: str, is_dark: bool):
        """Build a card for a single issue"""
        return build_issue_card(issue, emoji, color, is_dark)

    def _format_report_as_text(self) -> str:
        """Format the health report as plain text for export."""
        return format_health_report(self.health_report)

    def _on_save_report(self, e):
        """Handle save report button click - open file picker and save report."""
        if not self.health_report:
            return

        try:
            # Generate default filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            default_name = f"health_report_{timestamp}.txt"

            # Open save dialog
            file_path = save_file_dialog(default_name)

            if file_path:
                # Format and save the report
                report_text = self._format_report_as_text()

                print(f"Report text length: {len(report_text)} characters")
                print(f"Attempting to save to: {file_path}")

                # Ensure parent directory exists
                file_path.parent.mkdir(parents=True, exist_ok=True)

                # Write report to file
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(report_text)

                print(f"File saved successfully to: {file_path}")
                if file_path.exists():
                    print(f"File size: {file_path.stat().st_size} bytes")

                # Show success message
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"Report saved to {file_path.name}"),
                    bgcolor=Colors.GREEN_500,
                )
                self.page.snack_bar.open = True
                self.page.update()

        except Exception as ex:
            print(f"Failed to save report - Exception: {str(ex)}")
            import traceback
            traceback.print_exc()
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Error saving report: {str(ex)}"),
                bgcolor=Colors.RED_500,
            )
            self.page.snack_bar.open = True
            self.page.update()

    def _build_setup_prompt(self) -> ft.Container:
        """Build UI prompting user to run setup wizard"""
        is_dark = self.page.theme_mode == ft.ThemeMode.DARK

        return ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.FOLDER_ROUNDED, size=64, color=Colors.ACCENT_500),
                ft.Text(
                    "Code Project Detected",
                    size=Typography.H2,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Text(
                    "This folder contains code but no Claude Code configuration.",
                    size=Typography.BODY_MD,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    "Would you like to set up Claude Code for this project?",
                    size=Typography.BODY_MD,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Container(height=Spacing.MD),
                ft.Row([
                    ft.ElevatedButton(
                        "No, Cancel",
                        on_click=lambda e: self._clear_results()
                    ),
                    ft.ElevatedButton(
                        "Yes, Set Up Claude Code",
                        icon=ft.Icons.ROCKET_LAUNCH_ROUNDED,
                        on_click=lambda e: self._navigate_to_wizard(),
                        bgcolor=Colors.ACCENT_500,
                    ),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=Spacing.MD),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=Spacing.MD),
            padding=Spacing.XL,
            alignment=ft.alignment.center,
        )

    def _navigate_to_wizard(self):
        """Navigate to wizard tab and pass selected path"""
        # Store path in app_state for wizard to pick up
        set_wizard_path(self.selected_path)

        # Navigate to wizard tab (index 4)
        if self.on_navigate:
            self.on_navigate(4)

    def _clear_results(self):
        """Clear scan results"""
        self.results_container.content = None
        self.page.update()

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
