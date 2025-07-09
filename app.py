import os
from flask import Flask, render_template, request
import numpy as np
from PIL import Image, ImageOps
import tensorflow as tf

# Load the model
model = tf.keras.models.load_model("mnist_model.keras")

# Create the Flask app
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  # Make sure index.html is in a folder named "templates"

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return 'No image uploaded', 400

    file = request.files['image']
    if file.filename == '':
        return 'No selected file', 400

    image = Image.open(file).convert('L')  # Convert to grayscale
    image = ImageOps.invert(image)         # Invert colors (MNIST expects white digits on black background)
    image = image.resize((28, 28))
    img_array = np.array(image)
    img_array = img_array.reshape(1, 28, 28, 1).astype('float32') / 255.0

    prediction = model.predict(img_array)
    predicted_digit = np.argmax(prediction)

    return render_template('index.html', prediction=predicted_digit)

if __name__ == '__main__':
    # Use the PORT provided by Render or fallback to 5000 locally
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

