#!/usr/bin/env bash
# Install the four mcm-plot-python OTF fonts for the CURRENT USER ONLY.
#
# No administrator rights are needed: the files go to
#   %LOCALAPPDATA%\Microsoft\Windows\Fonts
# and one value per face is added under
#   HKCU\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts
# Nothing outside that user-scoped directory/key is touched.
#
# It does NOT copy, move or rename the four files under .claude/**; it only
# copies their bytes into the user font directory.
#
# ★ THE REGISTRY VALUE NAME IS LOAD-BEARING (measured 2026-09-30, R2025b U5):
#   MATLAB's listfonts (via pf.fonts.getInstalledFontList, see listfonts.m)
#   derives the family name from the registry VALUE NAME, not from the file's
#   name table.  Registering the regular face as "TeXGyreTermesX Regular
#   (TrueType)" (the spelling a human would expect, and the spelling already
#   present in this key for other vendors' fonts) makes MATLAB list NOTHING;
#   registering it as "TeXGyreTermesX (TrueType)" makes the family appear and
#   makes MATLAB embed TeXGyreTermesX-Regular in exported PDFs.  Causal control
#   is in the probe report (delete the value -> the family disappears again).
#   The styled faces keep their style word.
#
# Run:
#   bash tests/m3-matlab-font-probe/install-user-fonts.sh
# Reverse:
#   bash tests/m3-matlab-font-probe/uninstall-user-fonts.sh
set -euo pipefail

# Git-for-Windows bash rewrites arguments that look like /v, /t, /d into paths,
# which makes reg.exe report "Invalid syntax".  Turn that off for this script.
export MSYS_NO_PATHCONV=1

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SRC="$ROOT/.claude/skills/mcm-plot-python/assets/fonts"
DEST="$LOCALAPPDATA/Microsoft/Windows/Fonts"
DEST_WIN="$(cygpath -w "$DEST")"
KEY='HKCU\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts'

mkdir -p "$DEST"

# value name under HKCU\...\Fonts   ->  file copied into the user font directory
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
  cp -f "$SRC/${FILES[$i]}" "$DEST/${FILES[$i]}"
  reg add "$KEY" /v "${VNAMES[$i]}" /t REG_SZ /d "${DEST_WIN}\\${FILES[$i]}" /f >/dev/null
  echo "installed: ${FILES[$i]}  as  [${VNAMES[$i]}]"
done

# Make the change visible to processes in this session (does NOT on its own make
# MATLAB list the font -- only the registry name above does; see report Q2/G).
MSYS_NO_PATHCONV=1 powershell -NoProfile -Command "
Add-Type -Namespace W -Name G3 -MemberDefinition '[DllImport(\"gdi32.dll\", CharSet=CharSet.Unicode)] public static extern int AddFontResourceEx(string f, uint fl, System.IntPtr r); [DllImport(\"user32.dll\")] public static extern System.IntPtr SendMessageTimeout(System.IntPtr h, uint msg, System.IntPtr w, System.IntPtr l, uint fl, uint t, out System.IntPtr res);' > \$null
\$d = Join-Path \$env:LOCALAPPDATA 'Microsoft\Windows\Fonts'
foreach (\$f in @('TeXGyreTermesX-Regular.otf','TeXGyreTermesX-Italic.otf','TeXGyreTermesX-Bold.otf','TeXGyreTermesX-BoldItalic.otf')) { [void][W.G3]::AddFontResourceEx((Join-Path \$d \$f), 0, [System.IntPtr]::Zero) }
\$r=[System.IntPtr]::Zero
[void][W.G3]::SendMessageTimeout([System.IntPtr]0xffff, 0x001D, [System.IntPtr]::Zero, [System.IntPtr]::Zero, 2, 1000, [ref]\$r)
" 2>/dev/null || echo "note: GDI refresh helper failed (not required for MATLAB to pick the font up)"

echo "done: ${#FILES[@]} files copied to $DEST_WIN, ${#VNAMES[@]} registry values added under $KEY"
