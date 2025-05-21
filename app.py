from flask import Flask, request, jsonify
from flask_cors import CORS
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import decode_predictions, preprocess_input
from tensorflow.keras.preprocessing import image
import numpy as np
import os
from datetime import datetime
import serial
import time

# Configura conexión serial al Arduino
# Asegúrate de cambiar '/dev/ttyUSB0' por el puerto correcto de tu sistema
# En Windows: 'COM3' o el que veas en el IDE de Arduino
arduino = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)  # Linux/macOS
# arduino = serial.Serial('COM3', 9600, timeout=1)  # Windows
time.sleep(2)  # Espera a que el Arduino se reinicie

app = Flask(__name__)
CORS(app)

# Carga el modelo de MobileNetV2 con pesos preentrenados en ImageNet
model = MobileNetV2(weights='imagenet')

# Listas simplificadas de razas
razas_gato = {
    "tabby", "tiger_cat", "Persian_cat", "Siamese_cat", "Egyptian_cat"
}

razas_perro = {
    "golden_retriever", "Labrador_retriever", "Chihuahua", "pug", "German_shepherd"
}


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
        # Preprocesamiento de imagen
        img = image.load_img(nombre_archivo, target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)

        # Predicción
        preds = model.predict(x)
        decoded = decode_predictions(preds, top=5)[0]

        resultado = "desconocido"
        for _, label, prob in decoded:
            if label in razas_gato:
                resultado = "gato"
                break
            elif 'dog' in label.lower() or label in razas_perro:
                resultado = "perro"
                break

        # Enviar al Arduino por serial
        if resultado == "gato":
            arduino.write(b'G\n')
        elif resultado == "perro":
            arduino.write(b'P\n')
        else:
            arduino.write(b'U\n')

        # Eliminar archivo
        os.remove(nombre_archivo)

        return jsonify({
            "resultado": resultado,
            "detalles": [(label, float(f"{prob:.4f}")) for (_, label, prob) in decoded]
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
