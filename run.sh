#!/bin/bash
# run.sh - Starts the AI Predictions Service

# ============================================================================
# Environment Setup
# ============================================================================

set -a
source .env 2>/dev/null || true  # Don't fail if .env doesn't exist
set +a

# ============================================================================
# Environment Setup
# ============================================================================

# Get the directory of this script (so it works anywhere)
DIR="$(cd "$(dirname "$0")" && pwd)"

# Set the PYTHONPATH to include the src directory
export PYTHONPATH="$DIR/service${PYTHONPATH:+:$PYTHONPATH}"

# ============================================================================
# Display Configuration
# ============================================================================

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 Starting Service"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📁 Script Directory: $DIR"
echo "🐍 PYTHONPATH:       $PYTHONPATH"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Run the main script using uv run (recommended for uv projects)
# Pass PYTHONPATH explicitly to ensure uv run uses it
PYTHONPATH="$DIR/service${PYTHONPATH:+:$PYTHONPATH}" uv run python "$DIR/service/main.py"
