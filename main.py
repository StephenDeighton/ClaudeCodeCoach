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
    page.bgcolor = Colors.LIGHT_BG

    # Show version in console
    print(f"🎯 Starting {get_version_string()}")

    # Placeholder UI
    page.add(
        ft.Container(
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.MEDICAL_SERVICES, size=64, color=Colors.ACCENT_500),
                    ft.Text(
                        "Claude Code Coach",
                        size=32,
                        weight=ft.FontWeight.BOLD,
                        color=Colors.TEXT_DARK,
                    ),
                    ft.Text(
                        "Ready for development",
                        size=16,
                        color=Colors.TEXT_DARK_MUTED,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=16,
            ),
            expand=True,
            alignment=ft.alignment.center,
        )
    )

    page.update()


if __name__ == "__main__":
    ft.app(target=main)
