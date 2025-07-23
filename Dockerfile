# Use official Python image
FROM python:3.9-slim

# Set work directory
WORKDIR /flask_api

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy app files
COPY . .

# Expose port
EXPOSE 5000

# Start the Flask app
CMD ["flask", "run"]
