"""
Issue Card Component
Displays a single health issue in scan results
"""

import flet as ft
from theme import Colors, Spacing, Radius, Typography


def build_issue_card(issue, emoji: str, color: str, is_dark: bool) -> ft.Container:
    """
    Build a card displaying a health issue.

    Args:
        issue: HealthIssue object
        emoji: Severity emoji (🔴/🟡/🔵)
        color: Card accent color
        is_dark: Dark mode flag

    Returns:
        Container with the issue card UI
    """
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
                                selectable=True,
                            ),
                            ft.Text(
                                issue.suggestion,
                                size=Typography.BODY_SM,
                                color=Colors.TEXT_DARK_MUTED if not is_dark else Colors.TEXT_LIGHT_MUTED,
                                selectable=True,
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
                                    selectable=True,
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
