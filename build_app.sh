#!/bin/bash
# Build script for ClaudeCodeCoach - Production build using pyproject.toml

echo "═══════════════════════════════════════════════════════════"
echo "🚀 ClaudeCodeCoach Production Build"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "📝 Exclusions managed via pyproject.toml [tool.flet.app]"
echo "   This ensures a clean, minimal app package"
echo ""

# Change to project directory
cd "$(dirname "$0")"

# Increment version
echo "📝 Incrementing build number..."
venv_312/bin/python services/version.py increment
if [ $? -ne 0 ]; then
    echo "❌ Failed to increment version"
    exit 1
fi
echo ""

# Copy updated version.json to assets (so it gets bundled)
echo "📋 Copying version.json to assets..."
cp version.json assets/version.json
echo ""

# Clean old build
echo "🧹 Cleaning old build..."
rm -rf build
echo ""

# Build the app - Exclusions read from pyproject.toml
echo "🔨 Building macOS app..."
echo "    (This may take 5-10 minutes, especially on slow networks)"
echo ""
venv_312/bin/flet build macos \
    --project ClaudeCodeCoach \
    --org com.coach \
    --product ClaudeCodeCoach \
    --build-version $(cat version.json | grep '"version"' | cut -d'"' -f4)

if [ $? -eq 0 ]; then
    echo ""
    echo "🎨 Installing custom app icon..."
    cp assets/app_icon.icns build/macos/ClaudeCodeCoach.app/Contents/Resources/AppIcon.icns
    if [ $? -eq 0 ]; then
        echo "✓ Custom icon installed"
    else
        echo "⚠️ Warning: Could not install custom icon"
    fi

    # Get final app size and file count
    APP_SIZE=$(du -sh build/macos/ClaudeCodeCoach.app | cut -f1)
    FILE_COUNT=$(unzip -l "build/macos/ClaudeCodeCoach.app/Contents/Frameworks/App.framework/Versions/A/Resources/flutter_assets/app/app.zip" 2>/dev/null | tail -1 | awk '{print $(NF-1)}')

    echo ""
    echo "═══════════════════════════════════════════════════════════"
    echo "✅ Build completed successfully!"
    echo "═══════════════════════════════════════════════════════════"
    echo ""
    echo "📦 App location: build/macos/ClaudeCodeCoach.app"
    echo "📊 App size: $APP_SIZE (target: ~300MB)"
    echo "📁 File count: $FILE_COUNT files (down from 17,755!)"
    echo "📊 Version: $(venv_312/bin/python services/version.py)"
    echo ""
    echo "💡 Exclusions configured in pyproject.toml [tool.flet.app]"
    echo ""
else
    echo ""
    echo "❌ Build failed!"
    echo "    Check your network connection and try again"
    exit 1
fi
