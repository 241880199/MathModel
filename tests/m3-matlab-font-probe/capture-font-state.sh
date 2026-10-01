#!/usr/bin/env bash
# Dump the exact per-user font state (registry values + user font directory) so
# that "before" and "after" can be diffed byte-for-byte.
#
# Run:
#   bash tests/m3-matlab-font-probe/capture-font-state.sh > <out.txt>
#
# The output is stable across runs on an unchanged machine, so a diff of two
# captures is a valid equality test (modulo reg.exe's leading blank line).
export MSYS_NO_PATHCONV=1

DEST="$LOCALAPPDATA/Microsoft/Windows/Fonts"
KEY='HKCU\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts'

echo "### HKCU Fonts key (reg query) ###"
reg query "$KEY" 2>&1
echo "### user font dir (ls -1) ###"
ls -1 "$DEST" 2>&1
echo "### user font dir (ls -la) ###"
ls -la "$DEST" 2>&1
echo "### HKLM Fonts: TeXGyre present? ###"
reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts" 2>&1 | grep -i "texgyre\|termes"
echo "(grep_rc=$?)"
