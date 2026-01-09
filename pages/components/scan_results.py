"""
Scan Results Display Components
Builds UI for health scan results and error states
"""

import flet as ft
from theme import Colors, Spacing, Radius, Typography
from health_checks.base import Severity
from services.health_checker import get_health_checker


def build_not_claude_project(is_dark: bool) -> ft.Container:
    """
    Build UI for non-Claude Code project error state.

    Args:
        is_dark: Dark mode flag

    Returns:
        Container with error message and icon
    """
    return ft.Container(
        content=ft.SelectionArea(
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
        ),
        padding=Spacing.XL,
        alignment=ft.alignment.center,
    )


def build_scan_results(
    health_report,
    is_dark: bool,
    build_issue_card_fn,
    on_save_report,
) -> ft.Container:
    """
    Build health scan results display with score, issues, and actions.

    Args:
        health_report: HealthReport object from health_checker
        is_dark: Dark mode flag
        build_issue_card_fn: Function to build issue card (issue, emoji, color, is_dark) -> Control
        on_save_report: Callback for save report button click

    Returns:
        Container with complete results UI
    """
    if not health_report:
        return None

    checker = get_health_checker()

    # Score indicator color
    score_color = checker.get_score_color(health_report.score)
    score_label = checker.get_score_label(health_report.score)

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
    critical_issues = [i for i in health_report.issues if i.severity == Severity.CRITICAL]
    warning_issues = [i for i in health_report.issues if i.severity == Severity.WARNING]
    info_issues = [i for i in health_report.issues if i.severity == Severity.INFO]

    for issues, severity, emoji, color in [
        (critical_issues, "CRITICAL", "🔴", Colors.RED_500),
        (warning_issues, "WARNING", "🟡", Colors.YELLOW_500),
        (info_issues, "INFO", "🔵", Colors.BLUE_500),
    ]:
        for issue in issues:
            issue_card = build_issue_card_fn(issue, emoji, color, is_dark)
            issue_cards.append(issue_card)

    # Build the controls list
    controls = [
        # Score header
        ft.Container(
            content=ft.Row(
                [
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(
                                    str(health_report.score),
                                    size=48,
                                    weight=ft.FontWeight.BOLD,
                                    color=indicator_color,
                                    selectable=True,
                                ),
                                ft.Text(
                                    "/ 100",
                                    size=Typography.BODY_MD,
                                    color=Colors.TEXT_DARK_MUTED if not is_dark else Colors.TEXT_LIGHT_MUTED,
                                    selectable=True,
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
                                selectable=True,
                            ),
                            ft.Text(
                                score_label,
                                size=Typography.H2,
                                weight=ft.FontWeight.BOLD,
                                color=Colors.TEXT_DARK if not is_dark else Colors.TEXT_LIGHT,
                                selectable=True,
                            ),
                            ft.Text(
                                f"{len(health_report.issues)} issues found",
                                size=Typography.BODY_SM,
                                color=Colors.TEXT_DARK_MUTED if not is_dark else Colors.TEXT_LIGHT_MUTED,
                                selectable=True,
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
        ft.Container(height=Spacing.SM),
        # Save report button
        ft.Container(
            content=ft.ElevatedButton(
                "Save Report",
                icon=ft.Icons.SAVE_ALT_ROUNDED,
                on_click=on_save_report,
            ),
            alignment=ft.alignment.center_right,
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
                            selectable=True,
                        ),
                        ft.Text(
                            "Your Claude Code project looks healthy.",
                            size=Typography.BODY_MD,
                            color=Colors.TEXT_DARK_MUTED if not is_dark else Colors.TEXT_LIGHT_MUTED,
                            selectable=True,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=Spacing.MD,
                ),
                padding=Spacing.XL,
                alignment=ft.alignment.center,
            )
        )

    # Results layout - wrap in SelectionArea to enable text selection
    return ft.Container(
        content=ft.SelectionArea(
            content=ft.Column(
                controls,
                spacing=Spacing.SM,
                scroll=ft.ScrollMode.AUTO,
            ),
        ),
        expand=True,
        padding=Spacing.MD,
    )
