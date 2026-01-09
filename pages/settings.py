"""
Settings Page for Claude Code Coach
Theme and appearance customization
"""

import flet as ft
from theme import Colors, Spacing, Radius, Typography, section_header, divider
from services.version import get_version_with_date


# Color schemes with geometric styling
COLOR_SCHEMES = {
    "coral": {"name": "Electric Coral", "color": "#FF6B35", "description": "Bold & energetic"},
    "cyan": {"name": "Cyber Cyan", "color": "#00D9C4", "description": "Fresh & modern"},
    "indigo": {"name": "Deep Indigo", "color": "#4F46E5", "description": "Professional & refined"},
    "emerald": {"name": "Emerald", "color": "#10B981", "description": "Natural & calm"},
    "amber": {"name": "Golden Amber", "color": "#F59E0B", "description": "Warm & inviting"},
    "rose": {"name": "Rose Pink", "color": "#EC4899", "description": "Bold & creative"},
}


class SettingsPage:
    def __init__(self, page: ft.Page, on_theme_change=None):
        self.page = page
        self.on_theme_change = on_theme_change
        self.current_color = "coral"
        self.color_buttons_container = ft.Row(wrap=True, spacing=Spacing.MD, run_spacing=Spacing.MD)
        self.theme_options_column = ft.Column(spacing=Spacing.SM)
        self.content_container = ft.Container()

    def _get_current_theme(self):
        if self.page.theme_mode == ft.ThemeMode.LIGHT:
            return "light"
        elif self.page.theme_mode == ft.ThemeMode.DARK:
            return "dark"
        return "system"

    def _set_theme_mode(self, mode: str):
        """Set theme mode and rebuild UI"""
        if mode == "light":
            self.page.theme_mode = ft.ThemeMode.LIGHT
            self.page.bgcolor = Colors.LIGHT_BG
        elif mode == "dark":
            self.page.theme_mode = ft.ThemeMode.DARK
            self.page.bgcolor = Colors.PRIMARY_800
        else:
            self.page.theme_mode = ft.ThemeMode.SYSTEM

        # Rebuild theme options to show new selection
        self._build_theme_options()
        self.page.update()

        if self.on_theme_change:
            self.on_theme_change()

    def _select_color(self, color_key: str):
        """Handle color scheme selection"""
        self.current_color = color_key
        scheme = COLOR_SCHEMES[color_key]

        self.page.theme = ft.Theme(color_scheme_seed=scheme["color"])
        self.page.dark_theme = ft.Theme(color_scheme_seed=scheme["color"])

        # Rebuild color buttons to show selection
        self._build_color_buttons()
        self.page.update()

        if self.on_theme_change:
            self.on_theme_change()

    def _build_theme_options(self):
        """Build theme option cards"""
        self.theme_options_column.controls.clear()

        options = [
            ("light", "Light Mode", ft.Icons.LIGHT_MODE_ROUNDED, "Bright and clean interface"),
            ("dark", "Dark Mode", ft.Icons.DARK_MODE_ROUNDED, "Easy on the eyes"),
            ("system", "System Auto", ft.Icons.SETTINGS_SUGGEST_ROUNDED, "Follow system preference"),
        ]

        current = self._get_current_theme()
        is_dark = self.page.theme_mode == ft.ThemeMode.DARK

        for value, label, icon, description in options:
            is_selected = current == value

            option_card = ft.GestureDetector(
                content=ft.Container(
                    content=ft.Row(
                        [
                            ft.Container(
                                content=ft.Icon(
                                    icon,
                                    size=20,
                                    color=Colors.ACCENT_500 if is_selected else (Colors.TEXT_DARK_MUTED if not is_dark else Colors.TEXT_LIGHT_MUTED),
                                ),
                                width=40,
                                height=40,
                                border_radius=Radius.MD,
                                bgcolor=ft.Colors.with_opacity(0.1, Colors.ACCENT_500) if is_selected else "transparent",
                                border=ft.border.all(2, Colors.ACCENT_500 if is_selected else (Colors.LIGHT_BORDER_STRONG if not is_dark else Colors.PRIMARY_500)),
                                alignment=ft.alignment.center,
                            ),
                            ft.Column(
                                [
                                    ft.Text(
                                        label,
                                        size=Typography.BODY_MD,
                                        weight=ft.FontWeight.W_600 if is_selected else ft.FontWeight.NORMAL,
                                        color=Colors.TEXT_DARK if not is_dark else Colors.TEXT_LIGHT,
                                    ),
                                    ft.Text(
                                        description,
                                        size=Typography.TINY,
                                        color=Colors.TEXT_DARK_MUTED if not is_dark else Colors.TEXT_LIGHT_MUTED,
                                    ),
                                ],
                                spacing=0,
                                expand=True,
                            ),
                            ft.Container(
                                content=ft.Icon(
                                    ft.Icons.CHECK_CIRCLE_ROUNDED if is_selected else ft.Icons.CIRCLE_OUTLINED,
                                    size=24,
                                    color=Colors.ACCENT_500 if is_selected else (Colors.TEXT_DARK_MUTED if not is_dark else Colors.TEXT_LIGHT_MUTED),
                                ),
                            ),
                        ],
                        spacing=Spacing.MD,
                    ),
                    padding=Spacing.MD,
                    border_radius=Radius.MD,
                    border=ft.border.all(
                        2,
                        Colors.ACCENT_500 if is_selected else (Colors.LIGHT_BORDER_STRONG if not is_dark else Colors.PRIMARY_500),
                    ),
                    bgcolor=ft.Colors.with_opacity(0.03, Colors.ACCENT_500) if is_selected else "transparent",
                ),
                on_tap=lambda e, v=value: self._set_theme_mode(v),
            )

            self.theme_options_column.controls.append(option_card)

    def _build_color_buttons(self):
        """Build color scheme buttons"""
        self.color_buttons_container.controls.clear()
        is_dark = self.page.theme_mode == ft.ThemeMode.DARK

        for color_key, scheme in COLOR_SCHEMES.items():
            is_selected = color_key == self.current_color

            color_button = ft.GestureDetector(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.Container(
                                width=60,
                                height=60,
                                bgcolor=scheme["color"],
                                border_radius=Radius.MD,
                                border=ft.border.all(
                                    3,
                                    Colors.ACCENT_500 if is_selected else (Colors.LIGHT_BORDER_STRONG if not is_dark else Colors.PRIMARY_500),
                                ),
                                shadow=ft.BoxShadow(
                                    spread_radius=0,
                                    blur_radius=8 if is_selected else 4,
                                    color=ft.Colors.with_opacity(0.3 if is_selected else 0.1, scheme["color"]),
                                    offset=ft.Offset(0, 2),
                                ),
                            ),
                            ft.Text(
                                scheme["name"],
                                size=Typography.TINY,
                                weight=ft.FontWeight.W_600 if is_selected else ft.FontWeight.NORMAL,
                                color=Colors.TEXT_DARK if not is_dark else Colors.TEXT_LIGHT,
                                text_align=ft.TextAlign.CENTER,
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=Spacing.XS,
                    ),
                    padding=Spacing.SM,
                ),
                on_tap=lambda e, ck=color_key: self._select_color(ck),
            )

            self.color_buttons_container.controls.append(color_button)

    def build(self) -> ft.Control:
        """Build settings page"""
        is_dark = self.page.theme_mode == ft.ThemeMode.DARK

        # Build theme options and color buttons
        self._build_theme_options()
        self._build_color_buttons()

        # Get version info
        version_text = get_version_with_date()

        # Main content
        content = ft.Container(
            content=ft.Column(
                [
                    # Header
                    section_header(
                        "Settings",
                        "Customize your experience",
                        ft.Icons.SETTINGS_ROUNDED,
                        Colors.ACCENT_500,
                        is_dark=is_dark,
                    ),
                    divider(is_dark=is_dark),
                    # Appearance section
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Row(
                                    [
                                        ft.Container(
                                            width=4,
                                            height=20,
                                            bgcolor=Colors.ACCENT_500,
                                            border_radius=Radius.SM,
                                        ),
                                        ft.Text(
                                            "APPEARANCE",
                                            size=Typography.CAPTION,
                                            weight=ft.FontWeight.BOLD,
                                            color=Colors.TEXT_DARK_MUTED if not is_dark else Colors.TEXT_LIGHT_MUTED,
                                        ),
                                    ],
                                    spacing=Spacing.SM,
                                ),
                                ft.Container(height=Spacing.SM),
                                self.theme_options_column,
                            ],
                            spacing=Spacing.SM,
                        ),
                        padding=Spacing.MD,
                    ),
                    ft.Container(height=Spacing.MD),
                    # Accent Color section
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Row(
                                    [
                                        ft.Container(
                                            width=4,
                                            height=20,
                                            bgcolor=Colors.ACCENT_500,
                                            border_radius=Radius.SM,
                                        ),
                                        ft.Text(
                                            "ACCENT COLOR",
                                            size=Typography.CAPTION,
                                            weight=ft.FontWeight.BOLD,
                                            color=Colors.TEXT_DARK_MUTED if not is_dark else Colors.TEXT_LIGHT_MUTED,
                                        ),
                                    ],
                                    spacing=Spacing.SM,
                                ),
                                ft.Container(height=Spacing.SM),
                                self.color_buttons_container,
                            ],
                            spacing=Spacing.SM,
                        ),
                        padding=Spacing.MD,
                    ),
                    # Version info
                    ft.Container(expand=True),
                    ft.Container(
                        content=ft.Text(
                            version_text,
                            size=Typography.TINY,
                            color=Colors.TEXT_DARK_MUTED if not is_dark else Colors.TEXT_LIGHT_MUTED,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        alignment=ft.alignment.center,
                        padding=Spacing.MD,
                    ),
                ],
                spacing=0,
                scroll=ft.ScrollMode.AUTO,
            ),
            expand=True,
        )

        return content
