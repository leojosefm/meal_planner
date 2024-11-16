# Use an official Python image for the script
FROM python:3.9-slim

# Set up working directory
WORKDIR /app

# Copy Python script and requirements (if any)
COPY load_ingredient.py .
COPY requirements.txt .

# Install necessary packages
RUN pip install -r requirements.txt

# Entry point for running the Python script
CMD ["python", "load_ingredient.py"]
