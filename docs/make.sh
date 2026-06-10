#!/usr/bin/env bash
set -euo pipefail

SPHINXBUILD="python -m sphinx"
SOURCEDIR="."
BUILDDIR="_build"

usage() {
    echo "Usage: ./make.sh [html|clean|live|install]"
    echo ""
    echo "  html     Build HTML documentation in _build/html"
    echo "  clean    Remove the _build directory"
    echo "  live     Local server with auto-rebuild (requires sphinx-autobuild)"
    echo "  install  Install documentation dependencies"
}

case "${1:-help}" in
    html)
        $SPHINXBUILD -b html "$SOURCEDIR" "$BUILDDIR/html" ${SPHINXOPTS:-}
        echo ""
        echo "Documentation built at $BUILDDIR/html/index.html"
        ;;
    clean)
        if [ -d "$BUILDDIR" ]; then
            rm -rf "$BUILDDIR"
            echo "_build directory removed."
        else
            echo "Nothing to clean."
        fi
        ;;
    live)
        python -m sphinx_autobuild "$SOURCEDIR" "$BUILDDIR/html" ${SPHINXOPTS:-} --open-browser
        ;;
    install)
        pip install -r requirements.txt
        ;;
    help|*)
        usage
        ;;
esac
