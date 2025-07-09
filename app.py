import os
from flask import Flask, render_template, request
import tensorflow as tf
import numpy as np
from PIL import Image, ImageOps

app = Flask(__name__)
model = tf.keras.models.load_model("mnist_model.keras")

@app.route("/", methods=["GET", "POST"])
def home():
    prediction = None
    if request.method == "POST":
        file = request.files.get("file")
        if file and file.filename:
            try:
                img = Image.open(file).convert("L")
                img = ImageOps.invert(img).resize((28, 28))
                arr = np.array(img).reshape(1, 28, 28, 1).astype("float32") / 255.0
                pred = model.predict(arr)
                prediction = int(np.argmax(pred))
            except Exception as e:
                prediction = f"Error processing image: {e}"
        else:
            prediction = "No file uploaded"

    return render_template("index.html", prediction=prediction)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
