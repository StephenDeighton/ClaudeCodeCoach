"""
Claude Code Coach (C3)
======================

Main entry point for the Claude Code Coach application.
"""

import flet as ft
from services.version import get_version_string
from theme import Colors, Spacing, Radius, Typography, get_theme
from pages.settings import SettingsPage
from pages.health_scan import HealthScanPage
from pages.fix_page import FixPage


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

    # Track dark mode state
    def is_dark():
        if page.theme_mode == ft.ThemeMode.DARK:
            return True
        elif page.theme_mode == ft.ThemeMode.LIGHT:
            return False
        return page.platform_brightness == ft.Brightness.DARK

    # Current page content container
    content_area = ft.Container(
        expand=True,
        padding=Spacing.XL,
        bgcolor=Colors.LIGHT_BG,
    )

    # Create page instances
    def on_theme_change():
        """Callback when theme changes - refresh UI"""
        update_theme_dependent_colors()
        page.update()

    health_scan_page = HealthScanPage(page)
    fix_page = FixPage(page)
    settings_page = SettingsPage(page, on_theme_change=on_theme_change)

    # Page mapping
    pages = {
        0: health_scan_page,
        1: fix_page,
        2: settings_page,
    }

    # Navigation state
    selected_index = 0

    def navigate(index: int):
        """Handle navigation changes"""
        nonlocal selected_index
        selected_index = index
        content_area.content = pages[index].build()
        update_nav_buttons()
        update_theme_dependent_colors()
        page.update()

    def update_theme_dependent_colors():
        """Update colors based on theme"""
        dark = is_dark()
        content_area.bgcolor = Colors.PRIMARY_800 if dark else Colors.LIGHT_BG
        header.bgcolor = Colors.PRIMARY_900 if dark else Colors.LIGHT_SURFACE
        nav_container.bgcolor = Colors.PRIMARY_900 if dark else Colors.LIGHT_SURFACE

        # Update border colors
        header.border = ft.border.only(bottom=ft.BorderSide(2, Colors.PRIMARY_700 if dark else Colors.LIGHT_BORDER_STRONG))
        nav_container.border = ft.border.only(right=ft.BorderSide(2, Colors.PRIMARY_700 if dark else Colors.LIGHT_BORDER_STRONG))

    def create_nav_button(icon_outlined, icon_filled, label: str, index: int):
        """Create a navigation button"""
        is_selected = index == selected_index
        dark = is_dark()

        if is_selected:
            bg_color = Colors.ACCENT_500
            icon_color = Colors.LIGHT_BG
            text_color = Colors.LIGHT_BG
            icon = icon_filled
        else:
            bg_color = "transparent"
            icon_color = Colors.TEXT_LIGHT if dark else Colors.TEXT_DARK
            text_color = Colors.TEXT_LIGHT if dark else Colors.TEXT_DARK
            icon = icon_outlined

        return ft.Container(
            content=ft.Column(
                [
                    ft.Container(
                        content=ft.Icon(icon, color=icon_color, size=22),
                        width=48,
                        height=48,
                        bgcolor=bg_color,
                        border_radius=Radius.MD,
                        alignment=ft.alignment.center,
                    ),
                    ft.Text(
                        label,
                        size=Typography.TINY,
                        weight=ft.FontWeight.W_600 if is_selected else ft.FontWeight.W_500,
                        color=text_color,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=Spacing.XS,
            ),
            on_click=lambda e, i=index: navigate(i),
            padding=Spacing.SM,
        )

    nav_buttons = ft.Column(spacing=Spacing.SM)

    def update_nav_buttons():
        """Update navigation buttons"""
        nav_buttons.controls = [
            create_nav_button(ft.Icons.SEARCH_ROUNDED, ft.Icons.SEARCH_ROUNDED, "Scan", 0),
            create_nav_button(ft.Icons.BUILD_CIRCLE_OUTLINED, ft.Icons.BUILD_CIRCLE_ROUNDED, "Fix", 1),
            create_nav_button(ft.Icons.SETTINGS_OUTLINED, ft.Icons.SETTINGS_ROUNDED, "Settings", 2),
        ]

    # Header
    header = ft.Container(
        content=ft.Row(
            [
                ft.Text(
                    "Claude Code Coach",
                    size=Typography.H1,
                    weight=ft.FontWeight.BOLD,
                    color=Colors.TEXT_LIGHT,
                ),
                ft.Container(expand=True),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.padding.symmetric(horizontal=Spacing.XL, vertical=Spacing.MD),
        bgcolor=Colors.PRIMARY_900,
        border=ft.border.only(bottom=ft.BorderSide(2, Colors.PRIMARY_700)),
    )

    # Navigation rail
    nav_container = ft.Container(
        content=ft.Column(
            [
                ft.Container(height=Spacing.MD),
                nav_buttons,
                ft.Container(expand=True),
                # Bottom accent
                ft.Container(
                    width=4,
                    height=40,
                    bgcolor=Colors.ACCENT_500,
                    border_radius=Radius.PILL,
                ),
                ft.Container(height=Spacing.MD),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        width=80,
        bgcolor=Colors.PRIMARY_900,
        border=ft.border.only(right=ft.BorderSide(2, Colors.PRIMARY_700)),
        padding=ft.padding.symmetric(vertical=Spacing.SM),
    )

    # Initialize
    update_nav_buttons()
    content_area.content = health_scan_page.build()
    update_theme_dependent_colors()

    # Main layout
    page.add(
        ft.Column(
            [
                header,
                ft.Row(
                    [
                        nav_container,
                        content_area,
                    ],
                    expand=True,
                    spacing=0,
                ),
            ],
            expand=True,
            spacing=0,
        )
    )

    page.update()


if __name__ == "__main__":
    ft.app(target=main)
