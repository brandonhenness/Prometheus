#!/bin/bash
set -e

# Define a file to store the last commit hash
LAST_COMMIT_FILE="tmp/last_commit_hash"

# Get the current commit hash (assuming the git repo is available in the container)
if git rev-parse HEAD > /dev/null 2>&1; then
  CURRENT_COMMIT=$(git rev-parse HEAD)
else
  echo "Git repository not available; running asset compilation by default."
  CURRENT_COMMIT=""
fi

# Read the last commit hash if the file exists
if [ -f "$LAST_COMMIT_FILE" ]; then
  LAST_COMMIT=$(cat "$LAST_COMMIT_FILE")
else
  LAST_COMMIT=""
fi

# Compare the current and last commit hashes
if [ "$CURRENT_COMMIT" != "$LAST_COMMIT" ]; then
  echo "Detected changes in the codebase. Running asset-related tasks..."
  
  echo "Installing Node modules for asset revisioning..."
  yarn install

  echo "Running asset rev..."
  yarn gulp rev

  # Update the stored commit hash if available
  if [ -n "$CURRENT_COMMIT" ]; then
    echo "$CURRENT_COMMIT" > "$LAST_COMMIT_FILE"
  fi
else
  echo "No changes detected. Skipping asset-related tasks."
fi

echo "Attempting to create the database..."
bin/rails db:create || true

echo "Running migrations..."
bin/rails db:migrate || true

if [ ! -f tmp/db_initial_setup_done ]; then
  echo "Running database initial setup..."
  bundle exec rake db:initial_setup
  touch tmp/db_initial_setup_done
fi

echo "Starting the application..."
exec "$@"
