#!/usr/bin/bash
set -e

REPO_URL="https://github.com/DobroSaBokja/pykiln"
BRANCH="prod"
TMP_DIR=$(mktemp -d)
INSTALL_LIB="/usr/lib/pykiln"
INSTALL_BIN="/usr/bin/kiln"

echo "Cloning pykiln ($BRANCH)..."
git clone --branch "$BRANCH" --depth 1 "$REPO_URL" "$TMP_DIR"

echo "Installing to $INSTALL_LIB..."
install -d "$INSTALL_LIB"
install -m 644 "$TMP_DIR/main.py" "$INSTALL_LIB/"
install -m 644 "$TMP_DIR/factories.py" "$INSTALL_LIB/"
install -m 644 "$TMP_DIR/xml_parser.py" "$INSTALL_LIB/"
install -m 644 "$TMP_DIR/widget_builder.py" "$INSTALL_LIB/"
install -m 644 "$TMP_DIR/lib.py" "$INSTALL_LIB/"
install -m 644 "$TMP_DIR/scripts.py" "$INSTALL_LIB/"

echo "Installing kiln to $INSTALL_BIN..."
install -m 755 "$TMP_DIR/kiln" "$INSTALL_BIN"

rm -rf "$TMP_DIR"
echo "Done. Run: kiln path/to/file.kiln"
