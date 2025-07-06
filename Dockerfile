FROM python:3.10-slim

# Install tesseract-ocr and its dependencies
RUN apt-get update && apt-get install -y tesseract-ocr libtesseract-dev && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your backend code
COPY . .

# Expose the port your app runs on
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]