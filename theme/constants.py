"""
Claude Code Coach - Design System Constants
Color palette, spacing, radius, and typography definitions
"""


# =============================================================================
# COLOR PALETTE - Bold & High Contrast
# =============================================================================

class Colors:
    """Bold geometric color system"""

    # Primary - Deep Navy/Indigo
    PRIMARY_900 = "#0F0D1A"      # Darkest - near black
    PRIMARY_800 = "#1A1726"      # Dark background
    PRIMARY_700 = "#252136"      # Elevated surface dark
    PRIMARY_600 = "#312B48"      # Card dark
    PRIMARY_500 = "#433C5C"      # Muted elements

    # Accent - Electric Coral/Orange
    ACCENT_500 = "#FF6B35"       # Primary accent
    ACCENT_400 = "#FF8A5C"       # Lighter accent
    ACCENT_600 = "#E55A2B"       # Darker accent

    # Secondary Accent - Cyan/Teal
    SECONDARY_500 = "#00D9C4"    # Secondary accent
    SECONDARY_400 = "#33E3D2"    # Lighter
    SECONDARY_600 = "#00B8A5"    # Darker

    # Light Theme - Sepia/Parchment
    LIGHT_BG = "#EDE8DC"         # Warm sepia/parchment background
    LIGHT_SURFACE = "#F5F1E6"    # Cream paper for cards
    LIGHT_ELEVATED = "#FAF8F2"   # Light cream elevated
    LIGHT_BORDER = "#DDD5C5"     # Warm tan borders
    LIGHT_BORDER_STRONG = "#C9BFAB"  # Darker sepia borders

    # Text Colors
    TEXT_DARK = "#2D2418"        # Darker brown-black text for better contrast
    TEXT_DARK_MUTED = "#5D5347"  # Darker sepia muted text (was #7D7163)
    TEXT_LIGHT = "#F8F7FC"       # Primary text on dark
    TEXT_LIGHT_MUTED = "#B8B3C8" # Lighter secondary text on dark for better contrast

    # Semantic Colors
    SUCCESS = "#10B981"          # Green
    WARNING = "#F59E0B"          # Amber
    ERROR = "#EF4444"            # Red
    INFO = "#3B82F6"             # Blue

    # Content Type Colors (for icons/badges)
    EMAIL_COLOR = "#3B82F6"      # Blue
    DOCUMENT_COLOR = "#10B981"   # Green
    IMAGE_COLOR = "#8B5CF6"      # Purple
    VIDEO_COLOR = "#EF4444"      # Red
    CODE_COLOR = "#F59E0B"       # Amber
    FOLDER_COLOR = "#F59E0B"     # Amber

    # Status Colors (for health scores, indicators)
    GREEN_500 = "#10B981"        # Success/Healthy
    YELLOW_500 = "#F59E0B"       # Warning/Caution
    ORANGE_500 = "#F97316"       # Moderate concern
    RED_500 = "#EF4444"          # Critical/Error
    BLUE_500 = "#3B82F6"         # Info


# =============================================================================
# SPACING & SIZING
# =============================================================================

class Spacing:
    """Consistent spacing system"""
    XS = 4
    SM = 8
    MD = 12
    LG = 16
    XL = 24
    XXL = 32
    XXXL = 48


class Radius:
    """Border radius - geometric with some softness"""
    NONE = 0
    SM = 4
    MD = 8
    LG = 12
    XL = 16
    PILL = 100


# =============================================================================
# TYPOGRAPHY
# =============================================================================

class Typography:
    """Typography scale"""
    # Display
    DISPLAY_LG = 32
    DISPLAY_MD = 28
    DISPLAY_SM = 24

    # Headings
    H1 = 22
    H2 = 18
    H3 = 16

    # Body
    BODY_LG = 15
    BODY_MD = 14
    BODY_SM = 13

    # Caption/Small
    CAPTION = 12
    TINY = 11
