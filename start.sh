#!/bin/bash

# Start the Flask server
echo "Starting Flask server..."
python app.py

# If the Flask server crashes, this script will exit, and Docker Compose will restart the container