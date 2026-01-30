#!/bin/bash
# Script to reset and reseed the database

set -e

echo "🔄 Resetting and reseeding the database..."
echo ""

# Check if we're in docker or local
if [ -f /.dockerenv ]; then
    echo "📦 Running inside Docker container"
    PYTHON_CMD="python"
else
    echo "💻 Running locally"
    PYTHON_CMD="python"
fi

# Function to confirm action
confirm() {
    read -p "⚠️  This will DROP all tables and reseed the database. Continue? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ Aborted."
        exit 1
    fi
}

# Ask for confirmation
confirm

echo ""
echo "1️⃣  Downgrading database (dropping all tables)..."
alembic downgrade base

echo ""
echo "2️⃣  Running migrations (creating tables)..."
alembic upgrade head

echo ""
echo "3️⃣  Seeding database with initial data..."
$PYTHON_CMD seed_database.py --force

echo ""
echo "✅ Database reset and reseeded successfully!"
echo ""
echo "🎉 You can now use the application with fresh seed data."
