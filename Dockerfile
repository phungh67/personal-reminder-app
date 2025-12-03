# Use an official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.10-slim

# Set environment variables to prevent Python from writing pyc files to disc
# and buffering stdout/stderr.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application using Gunicorn (Production server)
# "run:app" points to run.py and the 'app' instance inside it
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]