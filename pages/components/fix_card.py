"""
Fix Card Component
Displays a single health issue with fix prompt and actions
"""

import flet as ft
from theme import Colors, Spacing, Radius, Typography


def build_fix_card(
    issue,
    emoji: str,
    color: str,
    is_dark: bool,
    selected_issues: dict,
    on_issue_selected,
    on_copy_to_clipboard,
) -> ft.Container:
    """
    Build a card for a single issue with fix prompt.

    Args:
        issue: HealthIssue object
        emoji: Severity emoji (🔴/🟡/🔵)
        color: Card accent color
        is_dark: Dark mode flag
        selected_issues: Dict of selected issue IDs
        on_issue_selected: Callback for checkbox change (e, issue)
        on_copy_to_clipboard: Callback for copy button (prompt, title)

    Returns:
        Container with the fix card UI
    """
    has_fix_prompt = issue.fix_prompt is not None and issue.fix_prompt.strip() != ""

    # Create checkbox for this issue
    checkbox = ft.Checkbox(
        value=selected_issues.get(issue.rule_id, False),
        on_change=lambda e: on_issue_selected(e, issue),
    )

    # Build the card content
    card_controls = [
        # Header with checkbox
        ft.Row(
            [
                checkbox,
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
            spacing=Spacing.SM,
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
                                    on_click=lambda e, prompt=issue.fix_prompt, title=issue.title: on_copy_to_clipboard(prompt, title),
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
