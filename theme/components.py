"""
Claude Code Coach - Styled UI Components
Reusable component builders with consistent styling
"""

import flet as ft
from .constants import Colors, Spacing, Radius, Typography


# =============================================================================
# COMPONENT STYLES
# =============================================================================

def get_theme(is_dark: bool) -> ft.Theme:
    """Get theme configuration"""
    if is_dark:
        return ft.Theme(
            color_scheme_seed=Colors.ACCENT_500,
        )
    else:
        return ft.Theme(
            color_scheme_seed=Colors.ACCENT_500,
        )


def styled_text_field(
    label: str,
    hint_text: str = "",
    expand: bool = False,
    width: int = None,
    on_change=None,
    is_dark: bool = False,
) -> ft.TextField:
    """Create a styled text field with geometric design"""
    return ft.TextField(
        label=label,
        hint_text=hint_text,
        expand=expand,
        width=width,
        on_change=on_change,
        border_radius=Radius.MD,
        border_width=2,
        border_color=Colors.LIGHT_BORDER_STRONG if not is_dark else Colors.PRIMARY_500,
        focused_border_color=Colors.ACCENT_500,
        cursor_color=Colors.ACCENT_500,
        label_style=ft.TextStyle(
            size=Typography.CAPTION,
            weight=ft.FontWeight.W_600,
        ),
    )


def styled_dropdown(
    label: str,
    value: str,
    options: list,
    width: int = None,
    on_change=None,
    is_dark: bool = False,
) -> ft.Dropdown:
    """Create a styled dropdown with geometric design"""
    return ft.Dropdown(
        label=label,
        value=value,
        options=options,
        width=width,
        on_change=on_change,
        border_radius=Radius.MD,
        border_width=2,
        border_color=Colors.LIGHT_BORDER_STRONG if not is_dark else Colors.PRIMARY_500,
        focused_border_color=Colors.ACCENT_500,
        label_style=ft.TextStyle(
            size=Typography.CAPTION,
            weight=ft.FontWeight.W_600,
        ),
    )


def primary_button(
    text: str,
    icon=None,
    on_click=None,
    disabled: bool = False,
) -> ft.ElevatedButton:
    """Primary action button with bold styling"""
    return ft.ElevatedButton(
        text=text,
        icon=icon,
        on_click=on_click,
        disabled=disabled,
        bgcolor=Colors.ACCENT_500,
        color=Colors.LIGHT_BG,
        style=ft.ButtonStyle(
            padding=ft.padding.symmetric(horizontal=Spacing.XL, vertical=Spacing.LG),
            shape=ft.RoundedRectangleBorder(radius=Radius.MD),
            elevation=0,
            overlay_color=Colors.ACCENT_600,
        ),
    )


def secondary_button(
    text: str,
    icon=None,
    on_click=None,
    disabled: bool = False,
) -> ft.OutlinedButton:
    """Secondary action button"""
    return ft.OutlinedButton(
        text=text,
        icon=icon,
        on_click=on_click,
        disabled=disabled,
        style=ft.ButtonStyle(
            padding=ft.padding.symmetric(horizontal=Spacing.LG, vertical=Spacing.LG),
            shape=ft.RoundedRectangleBorder(radius=Radius.MD),
            side=ft.BorderSide(width=2, color=Colors.ACCENT_500),
        ),
    )


def ghost_button(
    text: str,
    icon=None,
    on_click=None,
    color: str = None,
) -> ft.TextButton:
    """Ghost/text button"""
    return ft.TextButton(
        text=text,
        icon=icon,
        icon_color=color or Colors.ACCENT_500,
        on_click=on_click,
        style=ft.ButtonStyle(
            padding=ft.padding.symmetric(horizontal=Spacing.MD, vertical=Spacing.SM),
            shape=ft.RoundedRectangleBorder(radius=Radius.SM),
        ),
    )


def card_container(
    content: ft.Control,
    is_dark: bool = False,
    accent_color: str = None,
    padding: int = Spacing.LG,
) -> ft.Container:
    """Styled card with geometric design"""
    border_color = accent_color or (Colors.PRIMARY_500 if is_dark else Colors.LIGHT_BORDER_STRONG)
    bg_color = Colors.PRIMARY_700 if is_dark else Colors.LIGHT_SURFACE

    return ft.Container(
        content=content,
        padding=padding,
        border_radius=Radius.LG,
        bgcolor=bg_color,
        border=ft.border.all(2, border_color),
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=12,
            color=ft.Colors.with_opacity(0.08 if not is_dark else 0.3, "#000000"),
            offset=ft.Offset(0, 4),
        ),
    )


def section_header(
    title: str,
    subtitle: str = None,
    icon: str = None,
    icon_color: str = None,
    is_dark: bool = False,
) -> ft.Control:
    """Section header with bold typography"""
    text_color = Colors.TEXT_LIGHT if is_dark else Colors.TEXT_DARK
    muted_color = Colors.TEXT_LIGHT_MUTED if is_dark else Colors.TEXT_DARK_MUTED

    content = [
        ft.Row(
            [
                ft.Icon(icon, size=24, color=icon_color or Colors.ACCENT_500) if icon else ft.Container(),
                ft.Text(
                    title,
                    size=Typography.H1,
                    weight=ft.FontWeight.BOLD,
                    color=text_color,
                ),
            ],
            spacing=Spacing.SM,
        ),
    ]

    if subtitle:
        content.append(
            ft.Text(
                subtitle,
                size=Typography.BODY_SM,
                color=muted_color,
            )
        )

    return ft.Column(content, spacing=Spacing.XS)


def divider(is_dark: bool = False) -> ft.Container:
    """Styled divider with geometric accent"""
    color = Colors.PRIMARY_500 if is_dark else Colors.LIGHT_BORDER_STRONG
    return ft.Container(
        content=ft.Row(
            [
                ft.Container(
                    width=40,
                    height=3,
                    bgcolor=Colors.ACCENT_500,
                    border_radius=Radius.PILL,
                ),
                ft.Container(
                    expand=True,
                    height=1,
                    bgcolor=color,
                ),
            ],
            spacing=Spacing.SM,
        ),
        margin=ft.margin.symmetric(vertical=Spacing.MD),
    )


def badge(
    text: str,
    color: str = None,
    is_dark: bool = False,
) -> ft.Container:
    """Small badge/chip component"""
    bg = color or Colors.ACCENT_500
    return ft.Container(
        content=ft.Text(
            text,
            size=Typography.TINY,
            weight=ft.FontWeight.W_600,
            color=Colors.LIGHT_BG,
        ),
        bgcolor=bg,
        padding=ft.padding.symmetric(horizontal=Spacing.SM, vertical=Spacing.XS),
        border_radius=Radius.SM,
    )


def content_type_icon(content_class: str, size: int = 22) -> tuple:
    """Get icon and color for content type"""
    icons_map = {
        'email': (ft.Icons.EMAIL_ROUNDED, Colors.EMAIL_COLOR),
        'document': (ft.Icons.DESCRIPTION_ROUNDED, Colors.DOCUMENT_COLOR),
        'image': (ft.Icons.IMAGE_ROUNDED, Colors.IMAGE_COLOR),
        'video': (ft.Icons.VIDEO_FILE_ROUNDED, Colors.VIDEO_COLOR),
        'code': (ft.Icons.CODE_ROUNDED, Colors.CODE_COLOR),
        'folder': (ft.Icons.FOLDER_ROUNDED, Colors.FOLDER_COLOR),
    }
    icon, color = icons_map.get(content_class, (ft.Icons.INSERT_DRIVE_FILE_ROUNDED, Colors.TEXT_DARK_MUTED))
    return ft.Icon(icon, color=color, size=size), color


def result_card(
    content: ft.Control,
    is_dark: bool = False,
    index: int = 0,
    accent_color: str = None,
) -> ft.Container:
    """Result card with geometric accent stripe"""
    stripe_color = accent_color or Colors.ACCENT_500

    return ft.Container(
        content=ft.Row(
            [
                # Accent stripe
                ft.Container(
                    width=4,
                    height=None,
                    bgcolor=stripe_color,
                    border_radius=ft.border_radius.only(
                        top_left=Radius.LG,
                        bottom_left=Radius.LG,
                    ),
                ),
                # Content
                ft.Container(
                    content=content,
                    expand=True,
                    padding=Spacing.LG,
                ),
            ],
            spacing=0,
        ),
        border_radius=Radius.LG,
        border=ft.border.all(1, ft.Colors.OUTLINE_VARIANT),
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
    )
