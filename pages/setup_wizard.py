"""
Setup Wizard Page

Multi-step wizard for setting up Claude Code configuration in new projects.
Analyzes folder structure, detects tech stack, and generates appropriate
configuration files.
"""

import flet as ft
from pathlib import Path
import subprocess

from theme import Colors, Typography, Spacing
from services.tech_stack_analyzer import get_tech_stack_analyzer, TechStackInfo
from services.project_setup_service import get_project_setup_service, SetupResult
from services.status_updater import get_status_updater
from services.app_state import get_wizard_path, clear_wizard_path


class SetupWizardPage:
    """CC Setup Wizard - guides users through Claude Code configuration"""

    def __init__(self, page: ft.Page, on_navigate=None):
        self.page = page
        self.on_navigate = on_navigate

        # State
        self.selected_path = None
        self.tech_info = None
        self.setup_result = None
        self.current_step = 0  # 0=select, 1=analyze, 2=confirm, 3=progress, 4=complete

        # Services
        self.tech_analyzer = get_tech_stack_analyzer()
        self.setup_service = get_project_setup_service()
        self.status_updater = get_status_updater()

        # UI Components
        self.path_display = ft.Text("No directory selected", size=Typography.BODY_MD)
        self.content_container = ft.Container()

        # Check if path was passed from health scan
        wizard_path = get_wizard_path()
        if wizard_path:
            self.selected_path = wizard_path
            self.path_display.value = str(wizard_path)
            clear_wizard_path()

            # Auto-analyze the passed path
            self.tech_info = self.tech_analyzer.analyze_directory(self.selected_path)
            self.current_step = 1  # Move to analysis results

    def build(self) -> ft.Control:
        """Build wizard UI"""
        is_dark = self.page.theme_mode == ft.ThemeMode.DARK

        # Build step content
        if self.current_step == 0:
            step_content = self._build_step_selection()
        elif self.current_step == 1:
            step_content = self._build_step_analysis()
        elif self.current_step == 2:
            step_content = self._build_step_confirm()
        elif self.current_step == 3:
            step_content = self._build_step_progress()
        elif self.current_step == 4:
            step_content = self._build_step_complete()
        else:
            step_content = self._build_step_selection()

        # Main container
        content = ft.Container(
            content=ft.Column([
                # Header
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.ROCKET_LAUNCH_ROUNDED, size=32, color=Colors.ACCENT_500),
                        ft.Text(
                            "Claude Code Setup Wizard",
                            size=Typography.H1,
                            weight=ft.FontWeight.BOLD,
                        ),
                    ], spacing=Spacing.MD),
                    padding=ft.padding.only(bottom=Spacing.LG),
                ),

                # Step content
                self.content_container,
            ], spacing=Spacing.LG),
            padding=Spacing.XL,
            expand=True,
        )

        # Update content container
        self.content_container.content = step_content

        return content

    def _build_step_selection(self) -> ft.Control:
        """Step 0: Folder Selection"""
        is_dark = self.page.theme_mode == ft.ThemeMode.DARK

        return ft.Column([
            ft.Text(
                "Welcome! Let's set up Claude Code for your project.",
                size=Typography.H3,
            ),
            ft.Text(
                "This wizard will analyze your project and create an optimized Claude Code configuration.",
                size=Typography.BODY_MD,
            ),

            ft.Container(height=Spacing.LG),

            # Path display
            ft.Container(
                content=ft.Column([
                    ft.Text("Selected Directory:", weight=ft.FontWeight.BOLD),
                    self.path_display,
                ]),
                padding=Spacing.MD,
                border=ft.border.all(1, Colors.LIGHT_BORDER if not is_dark else Colors.PRIMARY_700),
                border_radius=Spacing.SM,
            ),

            ft.Container(height=Spacing.MD),

            # Buttons
            ft.Row([
                ft.ElevatedButton(
                    "Choose Directory",
                    icon=ft.Icons.FOLDER_OPEN_ROUNDED,
                    on_click=self._on_pick_directory,
                ),
                ft.ElevatedButton(
                    "Analyze Project",
                    icon=ft.Icons.ANALYTICS_OUTLINED,
                    on_click=self._on_analyze_click,
                    bgcolor=Colors.ACCENT_500,
                    disabled=self.selected_path is None,
                ),
            ], spacing=Spacing.MD),
        ], spacing=Spacing.MD)

    def _build_step_analysis(self) -> ft.Control:
        """Step 1: Analysis Results"""
        is_dark = self.page.theme_mode == ft.ThemeMode.DARK

        if not self.tech_info:
            return ft.Text("No analysis results")

        # Check if valid code project
        is_valid, reason = self.tech_analyzer.is_valid_code_project(self.tech_info)

        if not is_valid:
            # Show rejection message
            return self._build_rejection_ui(reason)

        # Build analysis results UI
        results = [
            ft.Icon(ft.Icons.CHECK_CIRCLE_ROUNDED, size=64, color=Colors.GREEN_500),
            ft.Text(
                "Valid Code Project Detected!",
                size=Typography.H2,
                weight=ft.FontWeight.BOLD,
            ),
            ft.Container(height=Spacing.MD),
        ]

        # Languages
        if self.tech_info.languages:
            lang_str = ", ".join(self.tech_info.languages)
            results.append(ft.Row([
                ft.Icon(ft.Icons.CODE_ROUNDED, color=Colors.ACCENT_500),
                ft.Text(f"Languages: {lang_str}", size=Typography.BODY_MD),
            ], spacing=Spacing.SM))

        # Package managers
        if self.tech_info.package_managers:
            pm_str = ", ".join(self.tech_info.package_managers)
            results.append(ft.Row([
                ft.Icon(ft.Icons.PACKAGE_ROUNDED, color=Colors.ACCENT_500),
                ft.Text(f"Package Managers: {pm_str}", size=Typography.BODY_MD),
            ], spacing=Spacing.SM))

        # Git
        git_status = "Yes" if self.tech_info.has_git else "No"
        git_icon = ft.Icons.CHECK_ROUNDED if self.tech_info.has_git else ft.Icons.CLOSE_ROUNDED
        results.append(ft.Row([
            ft.Icon(git_icon, color=Colors.ACCENT_500),
            ft.Text(f"Git Repository: {git_status}", size=Typography.BODY_MD),
        ], spacing=Spacing.SM))

        # File count
        results.append(ft.Row([
            ft.Icon(ft.Icons.INSERT_DRIVE_FILE_ROUNDED, color=Colors.ACCENT_500),
            ft.Text(f"Code Files: {self.tech_info.file_count}", size=Typography.BODY_MD),
        ], spacing=Spacing.SM))

        # Primary language
        if self.tech_info.primary_language:
            results.append(ft.Row([
                ft.Icon(ft.Icons.STAR_ROUNDED, color=Colors.ACCENT_500),
                ft.Text(f"Primary Language: {self.tech_info.primary_language}", size=Typography.BODY_MD),
            ], spacing=Spacing.SM))

        results.append(ft.Container(height=Spacing.LG))

        # Buttons
        results.append(ft.Row([
            ft.ElevatedButton(
                "Back",
                icon=ft.Icons.ARROW_BACK_ROUNDED,
                on_click=lambda e: self._change_step(0),
            ),
            ft.ElevatedButton(
                "Generate Setup",
                icon=ft.Icons.BUILD_CIRCLE_ROUNDED,
                on_click=self._on_generate_click,
                bgcolor=Colors.ACCENT_500,
            ),
        ], spacing=Spacing.MD))

        return ft.Column(results, spacing=Spacing.MD)

    def _build_rejection_ui(self, reason: str) -> ft.Control:
        """Build UI for rejected folder"""
        return ft.Column([
            ft.Icon(ft.Icons.ERROR_OUTLINE_ROUNDED, size=64, color=Colors.RED_500),
            ft.Text(
                "Invalid Project Folder",
                size=Typography.H2,
                weight=ft.FontWeight.BOLD,
            ),
            ft.Container(height=Spacing.MD),
            ft.Text(
                reason,
                size=Typography.BODY_MD,
                text_align=ft.TextAlign.CENTER,
            ),
            ft.Container(height=Spacing.MD),
            ft.Text(
                "This doesn't appear to be a code project. Please select a folder containing source code.",
                size=Typography.BODY_MD,
                text_align=ft.TextAlign.CENTER,
            ),
            ft.Container(height=Spacing.LG),
            ft.ElevatedButton(
                "Choose Different Folder",
                icon=ft.Icons.FOLDER_OPEN_ROUNDED,
                on_click=lambda e: self._change_step(0),
            ),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=Spacing.MD)

    def _build_step_confirm(self) -> ft.Control:
        """Step 2: Confirmation (for partial setup)"""
        is_dark = self.page.theme_mode == ft.ThemeMode.DARK

        if not self.selected_path:
            return ft.Text("No path selected")

        # Check for existing setup
        has_existing, existing_files = self.setup_service._check_existing_setup(self.selected_path)

        if not has_existing:
            # Skip confirmation, go straight to setup
            self._run_setup(overwrite=False)
            return self._build_step_progress()

        # Show overwrite warning
        file_list = [str(f.relative_to(self.selected_path)) for f in existing_files[:5]]

        return ft.Column([
            ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED, size=64, color=Colors.ORANGE_500),
            ft.Text(
                "Existing Setup Detected",
                size=Typography.H2,
                weight=ft.FontWeight.BOLD,
            ),
            ft.Container(height=Spacing.MD),
            ft.Text(
                "This project already has some Claude Code configuration.",
                size=Typography.BODY_MD,
            ),
            ft.Container(height=Spacing.SM),
            ft.Text(
                "Found:",
                size=Typography.BODY_MD,
                weight=ft.FontWeight.BOLD,
            ),
            *[ft.Text(f"• {f}", size=Typography.BODY_MD) for f in file_list],
            ft.Container(height=Spacing.MD),
            ft.Container(
                content=ft.Text(
                    "⚠ Continuing will overwrite existing configuration files with best practice defaults.",
                    size=Typography.BODY_MD,
                ),
                padding=Spacing.MD,
                bgcolor=Colors.ORANGE_500 + "20",
                border_radius=Spacing.SM,
            ),
            ft.Container(height=Spacing.LG),
            ft.Row([
                ft.ElevatedButton(
                    "Cancel",
                    icon=ft.Icons.CLOSE_ROUNDED,
                    on_click=lambda e: self._change_step(0),
                ),
                ft.ElevatedButton(
                    "Overwrite & Continue",
                    icon=ft.Icons.BUILD_CIRCLE_ROUNDED,
                    on_click=lambda e: self._run_setup(overwrite=True),
                    bgcolor=Colors.ORANGE_500,
                ),
            ], spacing=Spacing.MD),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=Spacing.MD)

    def _build_step_progress(self) -> ft.Control:
        """Step 3: Setup Progress"""
        if not self.setup_result:
            return ft.Column([
                ft.ProgressRing(),
                ft.Text("Generating configuration...", size=Typography.H3),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=Spacing.MD)

        # Show created files
        files_list = []
        for file_path in self.setup_result.files_created:
            rel_path = file_path.relative_to(self.selected_path) if self.selected_path else file_path
            files_list.append(ft.Row([
                ft.Icon(ft.Icons.CHECK_CIRCLE_ROUNDED, size=20, color=Colors.GREEN_500),
                ft.Text(str(rel_path), size=Typography.BODY_MD),
            ], spacing=Spacing.SM))

        return ft.Column([
            ft.Icon(ft.Icons.HOURGLASS_EMPTY_ROUNDED, size=64, color=Colors.ACCENT_500),
            ft.Text(
                "Generating Configuration...",
                size=Typography.H2,
                weight=ft.FontWeight.BOLD,
            ),
            ft.Container(height=Spacing.LG),
            *files_list,
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=Spacing.MD)

    def _build_step_complete(self) -> ft.Control:
        """Step 4: Completion"""
        if not self.setup_result:
            return ft.Text("No setup result")

        return ft.Column([
            ft.Icon(ft.Icons.CELEBRATION_ROUNDED, size=64, color=Colors.GREEN_500),
            ft.Text(
                "Setup Complete! 🎉",
                size=Typography.H2,
                weight=ft.FontWeight.BOLD,
            ),
            ft.Container(height=Spacing.MD),
            ft.Text(
                f"Created {len(self.setup_result.files_created)} files",
                size=Typography.BODY_MD,
            ),
            ft.Text(
                f"Expected health score: {self.setup_result.expected_score}/100",
                size=Typography.H3,
                weight=ft.FontWeight.BOLD,
                color=Colors.GREEN_500,
            ),
            ft.Container(height=Spacing.LG),
            ft.ElevatedButton(
                "Go to Scan Tab",
                icon=ft.Icons.SEARCH_ROUNDED,
                on_click=self._on_complete_click,
                bgcolor=Colors.ACCENT_500,
            ),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=Spacing.MD)

    # Event Handlers

    def _on_pick_directory(self, e):
        """Handle directory picker button click"""
        # Use macOS native folder picker (AppleScript workaround for Flet bug)
        try:
            script = '''
            tell application "System Events"
                activate
                set folderPath to POSIX path of (choose folder with prompt "Select project folder to set up Claude Code")
            end tell
            return folderPath
            '''

            result = subprocess.run(
                ['osascript', '-e', script],
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode == 0 and result.stdout.strip():
                folder_path = result.stdout.strip()
                self.selected_path = Path(folder_path)
                self.path_display.value = str(self.selected_path)
                self.page.update()
        except Exception as ex:
            print(f"Error picking directory: {ex}")

    def _on_analyze_click(self, e):
        """Handle analyze button click"""
        if not self.selected_path:
            return

        # Run tech stack analysis
        self.tech_info = self.tech_analyzer.analyze_directory(self.selected_path)

        # Move to analysis step
        self._change_step(1)

    def _on_generate_click(self, e):
        """Handle generate setup button click"""
        # Move to confirmation step (which checks for existing setup)
        self._change_step(2)

    def _run_setup(self, overwrite: bool):
        """Run the setup process"""
        if not self.selected_path or not self.tech_info:
            return

        # Move to progress step
        self._change_step(3)

        # Run setup
        self.setup_result = self.setup_service.setup_project(
            self.selected_path,
            self.tech_info,
            overwrite=overwrite
        )

        # Update status.md
        if self.setup_result.success:
            self.status_updater.append_setup_event(
                self.selected_path,
                self.tech_info,
                self.setup_result
            )

        # Move to complete step
        self._change_step(4)

    def _on_complete_click(self, e):
        """Handle completion button - navigate to scan tab"""
        if self.on_navigate:
            self.on_navigate(0)  # Navigate to Scan tab (index 0)

    def _change_step(self, step: int):
        """Change to a different step"""
        self.current_step = step

        # Rebuild the UI for the new step
        is_dark = self.page.theme_mode == ft.ThemeMode.DARK

        if self.current_step == 0:
            step_content = self._build_step_selection()
        elif self.current_step == 1:
            step_content = self._build_step_analysis()
        elif self.current_step == 2:
            step_content = self._build_step_confirm()
        elif self.current_step == 3:
            step_content = self._build_step_progress()
        elif self.current_step == 4:
            step_content = self._build_step_complete()
        else:
            step_content = self._build_step_selection()

        # Update the content container
        self.content_container.content = step_content
        self.page.update()


# Note: This page doesn't need explicit export - imported by main.py
