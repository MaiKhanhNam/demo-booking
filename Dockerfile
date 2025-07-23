# Use the official Python image as a base image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /home/nammk/source

# Copy requirements file to the working directory
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application
CMD ["gunicorn", "--reload", "-w", "4", "-b", "0.0.0.0:5000", "run:app"]