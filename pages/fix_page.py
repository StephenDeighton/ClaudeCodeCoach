"""
Fix Page for Claude Code Coach
Display issues with actionable fix prompts that can be copied
"""

import flet as ft
from theme import Colors, Spacing, Radius, Typography, section_header, divider
from services.app_state import get_last_scan
from health_checks.base import Severity
from pages.components.fix_card import build_fix_card
from pages.components.filter_controls import build_filter_controls


class FixPage:
    def __init__(self, page: ft.Page):
        self.page = page
        self.selected_severity = "All"  # Filter state
        self.sort_by = "severity"  # Sort state: "severity", "title"
        self.selected_issues = {}  # Dict[issue_id, bool] - track selected issues

        # UI components that need updating
        self.issues_container = ft.Container()
        self.stats_text = ft.Text()
        self.export_button = ft.ElevatedButton(
            "Export Selected (0)",
            icon=ft.Icons.CONTENT_COPY_ROUNDED,
            on_click=self._on_export_selected,
            disabled=True,
        )

    def _filter_and_sort_issues(self):
        """Filter and sort issues based on current selection."""
        scan_result = get_last_scan()
        if not scan_result:
            return []

        issues = scan_result.issues

        # Filter by severity
        if self.selected_severity != "All":
            issues = [i for i in issues if i.severity.value.upper() == self.selected_severity]

        # Sort
        if self.sort_by == "severity":
            # CRITICAL > WARNING > INFO
            severity_order = {Severity.CRITICAL: 0, Severity.WARNING: 1, Severity.INFO: 2}
            issues = sorted(issues, key=lambda i: severity_order[i.severity])
        elif self.sort_by == "title":
            issues = sorted(issues, key=lambda i: i.title.lower())

        return issues

    def _on_filter_change(self, e):
        """Handle severity filter change."""
        self.selected_severity = e.control.value
        self._refresh_issues()

    def _on_sort_change(self, e):
        """Handle sort order change."""
        self.sort_by = e.control.value
        self._refresh_issues()

    def _copy_to_clipboard(self, text: str, issue_title: str):
        """Copy text to clipboard and show snackbar."""
        self.page.set_clipboard(text)
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(f"Copied fix prompt for: {issue_title}"),
            bgcolor=Colors.GREEN_500,
        )
        self.page.snack_bar.open = True
        self.page.update()

    def _on_issue_selected(self, e, issue):
        """Handle issue selection checkbox change."""
        issue_id = issue.rule_id
        self.selected_issues[issue_id] = e.control.value

        # Update export button
        selected_count = sum(1 for selected in self.selected_issues.values() if selected)
        self.export_button.text = f"Export Selected ({selected_count})"
        self.export_button.disabled = selected_count == 0
        self.page.update()

    def _on_export_selected(self, e):
        """Export all selected fix prompts to clipboard."""
        scan_result = get_last_scan()
        if not scan_result:
            return

        # Get selected issues
        selected = [
            issue for issue in scan_result.issues
            if self.selected_issues.get(issue.rule_id, False)
        ]

        if not selected:
            return

        # Build combined export text
        lines = []
        lines.append("=" * 80)
        lines.append("CLAUDE CODE FIX PROMPTS - BATCH EXPORT")
        lines.append("=" * 80)
        lines.append(f"\nProject: {scan_result.project_path}")
        lines.append(f"Exported: {scan_result.scan_time.strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"Issues: {len(selected)} selected")
        lines.append("")

        for i, issue in enumerate(selected, 1):
            severity_emoji = {"CRITICAL": "🔴", "WARNING": "🟡", "INFO": "🔵"}
            emoji = severity_emoji.get(issue.severity.value.upper(), "⚪")

            lines.append("")
            lines.append("=" * 80)
            lines.append(f"{i}. {emoji} [{issue.severity.value.upper()}] {issue.title}")
            lines.append("=" * 80)
            lines.append(f"Rule ID: {issue.rule_id}")
            lines.append("")

            if issue.fix_prompt:
                lines.append(issue.fix_prompt.strip())
            else:
                lines.append(f"Suggestion: {issue.suggestion}")

            lines.append("")

        lines.append("=" * 80)
        lines.append("END OF BATCH EXPORT")
        lines.append("=" * 80)
        lines.append("")
        lines.append("Instructions:")
        lines.append("1. Copy this entire text block")
        lines.append("2. Paste into Claude Code")
        lines.append("3. Claude will address each issue systematically")
        lines.append("")

        combined_text = "\n".join(lines)

        # Copy to clipboard
        self.page.set_clipboard(combined_text)
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(f"Exported {len(selected)} fix prompts to clipboard!"),
            bgcolor=Colors.GREEN_500,
        )
        self.page.snack_bar.open = True
        self.page.update()

    def _refresh_issues(self):
        """Refresh the issues display."""
        filtered_issues = self._filter_and_sort_issues()
        scan_result = get_last_scan()
        is_dark = self.page.theme_mode == ft.ThemeMode.DARK

        # Update stats
        if scan_result:
            self.stats_text.value = f"Showing {len(filtered_issues)} of {len(scan_result.issues)} issues"
        else:
            self.stats_text.value = "No scan results"

        # Build issue cards
        if filtered_issues:
            issue_cards = []
            for issue in filtered_issues:
                # Get severity display info
                if issue.severity == Severity.CRITICAL:
                    emoji, color = "🔴", Colors.RED_500
                elif issue.severity == Severity.WARNING:
                    emoji, color = "🟡", Colors.YELLOW_500
                else:
                    emoji, color = "🔵", Colors.BLUE_500

                issue_card = self._build_fix_card(issue, emoji, color, is_dark)
                issue_cards.append(issue_card)

            self.issues_container.content = ft.Column(
                issue_cards,
                spacing=Spacing.MD,
                scroll=ft.ScrollMode.AUTO,
            )
        else:
            # No issues to show
            self.issues_container.content = ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(
                            ft.Icons.CHECK_CIRCLE_ROUNDED,
                            size=64,
                            color=Colors.GREEN_500,
                        ),
                        ft.Text(
                            "No Issues Match Filter" if scan_result else "No Scan Results",
                            size=Typography.H2,
                            weight=ft.FontWeight.BOLD,
                            color=Colors.TEXT_DARK if not is_dark else Colors.TEXT_LIGHT,
                        ),
                        ft.Text(
                            "Try adjusting your filters or run a health scan first." if scan_result else "Run a health scan from the Scan tab to see issues here.",
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

        self.page.update()

    def _build_fix_card(self, issue, emoji: str, color: str, is_dark: bool):
        """Build a card for a single issue with fix prompt."""
        return build_fix_card(
            issue=issue,
            emoji=emoji,
            color=color,
            is_dark=is_dark,
            selected_issues=self.selected_issues,
            on_issue_selected=self._on_issue_selected,
            on_copy_to_clipboard=self._copy_to_clipboard,
        )

    def build(self) -> ft.Control:
        """Build fix page."""
        scan_result = get_last_scan()
        is_dark = self.page.theme_mode == ft.ThemeMode.DARK

        # Count issues by severity
        critical_count = 0
        warning_count = 0
        info_count = 0
        if scan_result:
            critical_count = sum(1 for i in scan_result.issues if i.severity == Severity.CRITICAL)
            warning_count = sum(1 for i in scan_result.issues if i.severity == Severity.WARNING)
            info_count = sum(1 for i in scan_result.issues if i.severity == Severity.INFO)

        # Prepare issues display
        self._refresh_issues()

        # Build controls
        content = ft.Container(
            content=ft.Column(
                [
                    # Header
                    section_header(
                        "Fix Issues",
                        "Copy fix prompts to resolve detected issues",
                        ft.Icons.BUILD_CIRCLE_ROUNDED,
                        Colors.ACCENT_500,
                        is_dark=is_dark,
                    ),
                    divider(is_dark=is_dark),
                    # Filters and sort
                    build_filter_controls(
                        critical_count=critical_count,
                        warning_count=warning_count,
                        info_count=info_count,
                        on_filter_change=self._on_filter_change,
                        on_sort_change=self._on_sort_change,
                        export_button=self.export_button,
                        stats_text=self.stats_text,
                        is_dark=is_dark,
                    ),
                    ft.Container(height=Spacing.SM),
                    # Issues container
                    ft.Container(
                        content=self.issues_container,
                        expand=True,
                        padding=Spacing.MD,
                    ),
                ],
                spacing=0,
                scroll=ft.ScrollMode.AUTO,
                expand=True,
            ),
            expand=True,
        )

        return content
