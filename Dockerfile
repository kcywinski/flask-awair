# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set the working directory in the container
RUN apt-get update && apt-get install -y vim && rm -rf /var/lib/apt/lists/*
WORKDIR /app

# Copy only the requirements file to leverage Docker cache
COPY requirements.in /app/

# Install pip-tools and compile requirements.in to requirements.txt
RUN set -e && \
pip install pip-tools && \
pip-compile requirements.in

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Make the start script executable
RUN chmod +x /app/start.sh

# Expose the port the app runs on
EXPOSE 5000

# Use the start script as the entry point
CMD ["/app/start.sh"]