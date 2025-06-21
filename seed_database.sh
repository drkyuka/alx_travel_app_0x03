#!/bin/bash
# Script to seed the database using pipenv
# This script will populate the database with:
# - 19 Users
# - 12 Listings
# - 30 Bookings
# - 51 Reviews

# Set the directory to the project root
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR/.."

# Check if faker is installed
if ! pipenv run pip list | grep -q "Faker"; then
    echo "Installing Faker package..."
    pipenv install faker
fi

# Run the seed command
echo "Running seed command..."
pipenv run python alx_travel_app/manage.py seed

echo "Database seeding complete!"
