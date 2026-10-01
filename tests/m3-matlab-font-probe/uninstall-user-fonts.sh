#!/usr/bin/env bash
# Remove exactly what install-user-fonts.sh added: the four copied OTF files
# and the four HKCU registry values. Nothing else is touched.
#
# Run:
#   bash tests/m3-matlab-font-probe/uninstall-user-fonts.sh
set -uo pipefail

# See install-user-fonts.sh: stop MSYS from rewriting /v, /f into paths.
export MSYS_NO_PATHCONV=1

DEST="$LOCALAPPDATA/Microsoft/Windows/Fonts"
KEY='HKCU\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts'

VNAMES=(
  "TeXGyreTermesX (TrueType)"
  "TeXGyreTermesX Italic (TrueType)"
  "TeXGyreTermesX Bold (TrueType)"
  "TeXGyreTermesX Bold Italic (TrueType)"
)
FILES=(
  "TeXGyreTermesX-Regular.otf"
  "TeXGyreTermesX-Italic.otf"
  "TeXGyreTermesX-Bold.otf"
  "TeXGyreTermesX-BoldItalic.otf"
)

for i in "${!FILES[@]}"; do
  if reg delete "$KEY" /v "${VNAMES[$i]}" /f >/dev/null 2>&1; then
    echo "reg removed: [${VNAMES[$i]}]"
  else
    echo "reg absent : [${VNAMES[$i]}]"
  fi
  rm -f "$DEST/${FILES[$i]}"
  echo "file removed: ${FILES[$i]}"
done

echo "done: 4 files and 4 registry values removed"
