from flask import Flask, render_template, request
import tensorflow as tf
import numpy as np
from PIL import Image, ImageOps

app = Flask(__name__)
model = tf.keras.models.load_model("mnist_model.keras")

@app.route("/", methods=["GET", "POST"])
def index():
    digit = None
    if request.method == "POST":
        file = request.files["file"]
        image = Image.open(file).convert("L")
        image = ImageOps.invert(image).resize((28, 28))
        img_array = np.array(image) / 255.0
        prediction = model.predict(img_array.reshape(1, 28, 28, 1))
        digit = np.argmax(prediction)
    return render_template("index.html", digit=digit)

if __name__ == "__main__":
    app.run(debug=True)
