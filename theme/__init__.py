"""
Claude Code Coach - Design System
Bold geometric design language with sharp aesthetics

This module provides a centralized theme system for consistent UI styling.
"""

# Re-export all constants for backward compatibility
from .constants import (
    Colors,
    Spacing,
    Radius,
    Typography,
)

# Re-export all component builders
from .components import (
    get_theme,
    styled_text_field,
    styled_dropdown,
    primary_button,
    secondary_button,
    ghost_button,
    card_container,
    section_header,
    divider,
    badge,
    content_type_icon,
    result_card,
)

__all__ = [
    # Constants
    "Colors",
    "Spacing",
    "Radius",
    "Typography",
    # Components
    "get_theme",
    "styled_text_field",
    "styled_dropdown",
    "primary_button",
    "secondary_button",
    "ghost_button",
    "card_container",
    "section_header",
    "divider",
    "badge",
    "content_type_icon",
    "result_card",
]
