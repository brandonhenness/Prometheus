#!/bin/bash
set -e

echo "Attempting to create the database..."
# Create the database if it doesn't exist
bin/rails db:create || true

echo "Running migrations..."
# Run any pending migrations
bin/rails db:migrate || true

echo "Installing Node modules for asset revisioning..."
yarn install

echo "Running asset rev..."
# Update asset revisions
yarn gulp rev

# Check if initial setup has been performed already.
# This flag file will be created after the first successful run.
if [ ! -f tmp/db_initial_setup_done ]; then
  echo "Running database initial setup..."
  # Run the initial setup. Make sure required environment variables are pre-set.
  bundle exec rake db:initial_setup
  # Create a flag file so this step doesn't run again
  touch tmp/db_initial_setup_done
fi

echo "Starting the application..."
exec "$@"
