from flask import Flask, request, jsonify
from flask_cors import CORS  # Importar CORS
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import decode_predictions, preprocess_input
from tensorflow.keras.preprocessing import image
import numpy as np
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Habilitar CORS para todas las rutas

model = MobileNetV2(weights='imagenet')


@app.route('/imagen', methods=['POST'])
def recibir_imagen():
    if 'file' not in request.files:
        return jsonify({"error": "No se encontró archivo en la solicitud"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Nombre de archivo vacío"}), 400

    nombre_archivo = f"imagen_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    file.save(nombre_archivo)

    try:
        img = image.load_img(nombre_archivo, target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)

        preds = model.predict(x)
        decoded = decode_predictions(preds, top=3)[0]

        clases_validas = ['dog', 'cat']
        resultado = "desconocido"
        for _, label, prob in decoded:
            if any(animal in label.lower() for animal in clases_validas):
                resultado = label.lower()
                break

        os.remove(nombre_archivo)
        return jsonify({"resultado": resultado, "detalles": str(decoded)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')  # Usar HTTPS
