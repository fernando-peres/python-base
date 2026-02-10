#!/usr/bin/env bash
set -euo pipefail

# Resolve repo root (parent of directory containing this script)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "Project name (alphanumeric, hyphens, underscores only):"
read -r -p "Project name: " PROJECT_NAME

if [[ -z "${PROJECT_NAME// /}" ]]; then
  echo "Error: project name cannot be empty."
  exit 1
fi

# Sanitize: spaces -> hyphens, strip invalid chars (keep alphanumeric, hyphen, underscore)
SANITIZED_NAME=$(echo "$PROJECT_NAME" | tr ' ' '-' | sed 's/[^a-zA-Z0-9_-]//g' | sed 's/^-*//;s/-*$//')
if [[ -z "$SANITIZED_NAME" ]]; then
  echo "Error: project name contained no valid characters."
  exit 1
fi

cd "$REPO_ROOT"

if [[ ! -f .env.example ]]; then
  echo "Error: .env.example not found in repo root."
  exit 1
fi

for dest in .env .env.local; do
  if [[ -f "$dest" ]]; then
    echo "Overwriting $dest"
  fi
  cp .env.example "$dest"
done

# Set SERVICE_NAME in .env and .env.local (avoid sed replacement escaping by using awk)
for f in .env .env.local; do
  awk -v name="$SANITIZED_NAME" 'BEGIN{FS=OFS="="} $1=="SERVICE_NAME"{$2=name}1' "$f" > "$f.tmp" && mv "$f.tmp" "$f"
done

# Update project name in pyproject.toml (match current name = "..." so we only replace the value)
if [[ -f pyproject.toml ]]; then
  sed "s/^name = \".*\"/name = \"$SANITIZED_NAME\"/" pyproject.toml > pyproject.toml.tmp && mv pyproject.toml.tmp pyproject.toml
else
  echo "Warning: pyproject.toml not found, skipping."
fi

echo "Done. SERVICE_NAME and pyproject.toml name set to: $SANITIZED_NAME"
echo "Created/updated: .env, .env.local"
