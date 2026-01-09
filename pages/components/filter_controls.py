"""
Filter Controls Component
Builds filter and sort dropdowns for issue lists
"""

import flet as ft
from theme import Colors, Spacing, Typography


def build_filter_controls(
    critical_count: int,
    warning_count: int,
    info_count: int,
    on_filter_change,
    on_sort_change,
    export_button: ft.Control,
    stats_text: ft.Control,
    is_dark: bool,
) -> ft.Container:
    """
    Build filter and sort controls toolbar.

    Args:
        critical_count: Number of critical issues
        warning_count: Number of warning issues
        info_count: Number of info issues
        on_filter_change: Callback for filter dropdown change
        on_sort_change: Callback for sort dropdown change
        export_button: Export selected button control
        stats_text: Stats text control
        is_dark: Dark mode flag

    Returns:
        Container with filter controls toolbar
    """
    return ft.Container(
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
                            on_change=on_filter_change,
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
                            on_change=on_sort_change,
                            width=150,
                        ),
                    ],
                    spacing=Spacing.XS,
                ),
                ft.Container(width=Spacing.MD),
                # Export button
                export_button,
                ft.Container(expand=True),
                # Stats
                stats_text,
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.END,
        ),
        padding=Spacing.MD,
    )
