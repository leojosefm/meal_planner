# Use an official Python image for the script
FROM python:3.9-slim

# Set up working directory
WORKDIR /app

# Copy Python script and requirements (if any)
COPY load_ingredient.py .
COPY load_meal_category.py .
COPY requirements.txt .
COPY start.sh .

# Make the shell script executable
RUN chmod +x start.sh

# Install necessary packages
RUN pip install -r requirements.txt

# Entry point for running the Python scripts sequentially
CMD ["./start.sh"]
