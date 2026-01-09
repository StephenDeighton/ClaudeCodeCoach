"""
Fix Page for Claude Code Coach
Display issues with actionable fix prompts that can be copied
"""

import flet as ft
from theme import Colors, Spacing, Radius, Typography, section_header, divider
from services.app_state import get_last_scan
from health_checks.base import Severity


class FixPage:
    def __init__(self, page: ft.Page):
        self.page = page
        self.selected_severity = "All"  # Filter state
        self.sort_by = "severity"  # Sort state: "severity", "title"

        # UI components that need updating
        self.issues_container = ft.Container()
        self.stats_text = ft.Text()

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
        has_fix_prompt = issue.fix_prompt is not None and issue.fix_prompt.strip() != ""

        # Build the card content
        card_controls = [
            # Header
            ft.Row(
                [
                    ft.Text(emoji, size=24),
                    ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Text(
                                        issue.severity.value.upper(),
                                        size=Typography.CAPTION,
                                        weight=ft.FontWeight.BOLD,
                                        color=color,
                                        selectable=True,
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
                                        selectable=True,
                                    ),
                                ],
                                spacing=Spacing.SM,
                            ),
                            ft.Text(
                                issue.title,
                                size=Typography.BODY_LG,
                                weight=ft.FontWeight.BOLD,
                                color=Colors.TEXT_DARK if not is_dark else Colors.TEXT_LIGHT,
                                selectable=True,
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
                selectable=True,
            ),
        ]

        # Add fix prompt section if available
        if has_fix_prompt:
            card_controls.extend([
                ft.Container(height=Spacing.MD),
                # Fix prompt section
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Text(
                                        "🔧 Fix Prompt",
                                        size=Typography.BODY_SM,
                                        weight=ft.FontWeight.BOLD,
                                        color=Colors.TEXT_DARK if not is_dark else Colors.TEXT_LIGHT,
                                    ),
                                    ft.Container(expand=True),
                                    ft.ElevatedButton(
                                        "Copy Prompt",
                                        icon=ft.Icons.CONTENT_COPY_ROUNDED,
                                        on_click=lambda e, prompt=issue.fix_prompt, title=issue.title: self._copy_to_clipboard(prompt, title),
                                        height=32,
                                    ),
                                ],
                                spacing=Spacing.SM,
                            ),
                            ft.Container(height=Spacing.XS),
                            ft.Container(
                                content=ft.Text(
                                    issue.fix_prompt,
                                    size=Typography.BODY_SM,
                                    color=Colors.TEXT_DARK_MUTED if not is_dark else Colors.TEXT_LIGHT_MUTED,
                                    selectable=True,
                                    max_lines=5,
                                    overflow=ft.TextOverflow.ELLIPSIS,
                                ),
                                padding=Spacing.SM,
                                bgcolor=ft.Colors.with_opacity(0.5, Colors.PRIMARY_900 if is_dark else Colors.LIGHT_BORDER),
                                border_radius=Radius.SM,
                            ),
                        ],
                        spacing=Spacing.XS,
                    ),
                    padding=Spacing.MD,
                    bgcolor=ft.Colors.with_opacity(0.05, Colors.ACCENT_500),
                    border_radius=Radius.MD,
                    border=ft.border.all(1, ft.Colors.with_opacity(0.3, Colors.ACCENT_500)),
                ),
            ])
        else:
            # No fix prompt available
            card_controls.extend([
                ft.Container(height=Spacing.SM),
                ft.Container(
                    content=ft.Text(
                        "💡 " + issue.suggestion,
                        size=Typography.BODY_SM,
                        color=Colors.TEXT_DARK_MUTED if not is_dark else Colors.TEXT_LIGHT_MUTED,
                        selectable=True,
                    ),
                    padding=Spacing.MD,
                    bgcolor=ft.Colors.with_opacity(0.03, color),
                    border_radius=Radius.MD,
                    border=ft.border.all(1, ft.Colors.with_opacity(0.2, color)),
                ),
            ])

        return ft.Container(
            content=ft.Column(
                card_controls,
                spacing=Spacing.XS,
            ),
            padding=Spacing.MD,
            border=ft.border.all(2, Colors.LIGHT_BORDER_STRONG if not is_dark else Colors.PRIMARY_500),
            border_radius=Radius.MD,
            bgcolor=ft.Colors.with_opacity(0.02, color) if not is_dark else ft.Colors.with_opacity(0.05, color),
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
                    ft.Container(
                        content=ft.Row(
                            [
                                # Filter dropdown
                                ft.Column(
                                    [
                                        ft.Text(
                                            "Filter by Severity",
                                            size=Typography.CAPTION,
                                            weight=ft.FontWeight.BOLD,
                                            color=Colors.TEXT_DARK_MUTED if not is_dark else Colors.TEXT_LIGHT_MUTED,
                                        ),
                                        ft.Dropdown(
                                            value="All",
                                            options=[
                                                ft.dropdown.Option("All", f"All ({critical_count + warning_count + info_count})"),
                                                ft.dropdown.Option("CRITICAL", f"Critical ({critical_count})"),
                                                ft.dropdown.Option("WARNING", f"Warning ({warning_count})"),
                                                ft.dropdown.Option("INFO", f"Info ({info_count})"),
                                            ],
                                            on_change=self._on_filter_change,
                                            width=200,
                                        ),
                                    ],
                                    spacing=Spacing.XS,
                                ),
                                ft.Container(width=Spacing.MD),
                                # Sort dropdown
                                ft.Column(
                                    [
                                        ft.Text(
                                            "Sort by",
                                            size=Typography.CAPTION,
                                            weight=ft.FontWeight.BOLD,
                                            color=Colors.TEXT_DARK_MUTED if not is_dark else Colors.TEXT_LIGHT_MUTED,
                                        ),
                                        ft.Dropdown(
                                            value="severity",
                                            options=[
                                                ft.dropdown.Option("severity", "Severity"),
                                                ft.dropdown.Option("title", "Title"),
                                            ],
                                            on_change=self._on_sort_change,
                                            width=150,
                                        ),
                                    ],
                                    spacing=Spacing.XS,
                                ),
                                ft.Container(expand=True),
                                # Stats
                                self.stats_text,
                            ],
                            alignment=ft.MainAxisAlignment.START,
                            vertical_alignment=ft.CrossAxisAlignment.END,
                        ),
                        padding=Spacing.MD,
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
