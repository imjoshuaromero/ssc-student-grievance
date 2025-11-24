# Run this in PowerShell to execute the schema
# Make sure PostgreSQL bin directory is in your PATH

# Connect to PostgreSQL and create database
psql -U postgres -c "CREATE DATABASE grievance_system;"

# Run the schema script
psql -U postgres -d grievance_system -f "schema.sql"
