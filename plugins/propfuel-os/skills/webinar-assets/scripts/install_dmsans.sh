#!/usr/bin/env bash
# Installs the DM Sans variable font into the sandbox so BOTH pipelines render in the brand font:
#   - Python/PIL post-webinar templates read /root/.local/share/fonts/DMSans.ttf directly
#   - HTML pre-webinar templates resolve font-family 'DM Sans' through fontconfig (Chromium)
# Safe to run every session; it is a no-op if the font is already present.
set -e
FONT_DIR="$HOME/.local/share/fonts"
FONT_FILE="$FONT_DIR/DMSans.ttf"
mkdir -p "$FONT_DIR"
if [ ! -s "$FONT_FILE" ] && [ "$(uname)" = "Darwin" ] && [ -s "$HOME/Library/Fonts/DMSans-VariableFont_opsz,wght.ttf" ]; then
  cp "$HOME/Library/Fonts/DMSans-VariableFont_opsz,wght.ttf" "$FONT_FILE"
fi
if [ ! -s "$FONT_FILE" ]; then
  curl -sL -o "$FONT_FILE" \
    "https://raw.githubusercontent.com/google/fonts/main/ofl/dmsans/DMSans%5Bopsz,wght%5D.ttf"
fi
# The Python templates hard-code /root/.local/share/fonts/DMSans.ttf. Make sure that path exists too.
if [ "$HOME" != "/root" ]; then
  mkdir -p /root/.local/share/fonts 2>/dev/null && cp -n "$FONT_FILE" /root/.local/share/fonts/DMSans.ttf 2>/dev/null || true
fi
# macOS has no fontconfig: verify the file instead.
if command -v fc-list >/dev/null 2>&1; then
  fc-cache -f >/dev/null 2>&1 || true
  if fc-list | grep -qi "dm sans"; then
    echo "DM Sans installed: $FONT_FILE"
  else
    echo "WARNING: DM Sans not visible to fontconfig. HTML renders will fall back to Liberation Sans." >&2
    exit 1
  fi
elif [ -s "$FONT_FILE" ]; then
  echo "DM Sans installed: $FONT_FILE"
else
  echo "WARNING: DM Sans missing at $FONT_FILE" >&2
  exit 1
fi
