"""
Claude Code Coach (C3)
======================

Main entry point for the Claude Code Coach application.
"""

import flet as ft
from services.version import get_version_string
from theme import Colors, get_theme


def main(page: ft.Page):
    """Main application entry point"""

    # Configure page
    page.title = "Claude Code Coach"
    page.window.width = 1200
    page.window.height = 800
    page.window.min_width = 800
    page.window.min_height = 600
    page.padding = 0
    page.spacing = 0
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = get_theme(is_dark=False)
    page.dark_theme = get_theme(is_dark=True)
    page.bgcolor = Colors.LIGHT_BG

    # Show version in console
    print(f"🎯 Starting {get_version_string()}")

    # Theme toggle button
    def is_dark():
        return page.theme_mode == ft.ThemeMode.DARK

    def toggle_theme(e):
        if page.theme_mode == ft.ThemeMode.LIGHT:
            page.theme_mode = ft.ThemeMode.DARK
            page.bgcolor = Colors.PRIMARY_800
            theme_btn.icon = ft.Icons.LIGHT_MODE_ROUNDED
            theme_btn.icon_color = Colors.TEXT_LIGHT_MUTED
            # Update text colors
            title_text.color = Colors.TEXT_LIGHT
            subtitle_text.color = Colors.TEXT_LIGHT_MUTED
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
            page.bgcolor = Colors.LIGHT_BG
            theme_btn.icon = ft.Icons.DARK_MODE_ROUNDED
            theme_btn.icon_color = Colors.TEXT_DARK_MUTED
            # Update text colors
            title_text.color = Colors.TEXT_DARK
            subtitle_text.color = Colors.TEXT_DARK_MUTED
        page.update()

    theme_btn = ft.IconButton(
        icon=ft.Icons.DARK_MODE_ROUNDED,
        on_click=toggle_theme,
        tooltip="Toggle theme",
        icon_size=20,
        icon_color=Colors.TEXT_DARK_MUTED,
    )

    # Text elements that need color updates
    title_text = ft.Text(
        "Claude Code Coach",
        size=32,
        weight=ft.FontWeight.BOLD,
        color=Colors.TEXT_DARK,
    )

    subtitle_text = ft.Text(
        "Ready for development",
        size=16,
        color=Colors.TEXT_DARK_MUTED,
    )

    # Placeholder UI
    page.add(
        ft.Column(
            [
                # Header with theme toggle
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Container(expand=True),
                            theme_btn,
                        ],
                        alignment=ft.MainAxisAlignment.END,
                    ),
                    padding=10,
                ),
                # Main content
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Icon(ft.Icons.MEDICAL_SERVICES, size=64, color=Colors.ACCENT_500),
                            title_text,
                            subtitle_text,
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=16,
                    ),
                    expand=True,
                    alignment=ft.alignment.center,
                ),
            ],
            expand=True,
            spacing=0,
        )
    )

    page.update()


if __name__ == "__main__":
    ft.app(target=main)
