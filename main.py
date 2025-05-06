from flask import Flask, request, jsonify
import os
import easyocr
import cv2
import requests

# Inicialitzem el lector d'EasyOCR
reader = easyocr.Reader(['en'], gpu=False)
# IP del ESP32 (Asegúrate de cambiar esta dirección por la IP correcta del ESP32)
esp32_ip = "http://172.16.6.150/capture"


app = Flask(__name__)

@app.route('/activar_radar', methods=['GET'])
def activar_radar():
    print("Radar activado")
    # Hacer la solicitud HTTP GET al ESP32 para capturar la imagen
    response = requests.get(esp32_ip)

    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
        # Guardar la imagen en el disco duro
        with open("static\\uploads\\captura.jpg", "wb") as file:
            file.write(response.content)
        print("✅ Imagen guardada en captura.jpg")
    else:
        print("❌ Error al obtener la imagen:", response.status_code)
    return jsonify({"mensaje": "Radar activado"}) 


if __name__ == '__main__':
    app.run(debug=True)
