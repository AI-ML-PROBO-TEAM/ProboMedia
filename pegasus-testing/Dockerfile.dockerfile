# Use the official Python base image with Python 3.8.16
FROM python:3.8.16

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the container
COPY app.py .
COPY templates templates
COPY pegasustokenizer pegasustokenizer
COPY pegasusmodel pegasusmodel
# Expose the port that the Flask app runs on (change it if needed)
EXPOSE 8009

# Start the Flask application
CMD ["python", "app.py"]
