# ✅ Use the official TensorFlow Docker image with Python 3.10
FROM tensorflow/tensorflow:2.12.0

# Set working directory
WORKDIR /app

# Copy all files into the container
COPY . .

# Install additional dependencies (Flask, Pillow, etc.)
RUN pip install Flask pillow

# Expose the port your Flask app will run on
EXPOSE 10000

# Run your Flask app
CMD ["python", "app.py"]
