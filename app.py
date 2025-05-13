from flask import Flask, jsonify
import os
import requests
from datetime import datetime

esp32_ip = "http://172.16.3.220/capture"  # IP actual de la càmera

app = Flask(__name__)

@app.route('/activar_radar', methods=['GET'])
def activar_radar():
    print("📡 Radar activat")

    try:
        response = requests.get(esp32_ip, timeout=5)  # fa la captura

        if response.status_code == 200:
            upload_dir = "static/uploads"
            os.makedirs(upload_dir, exist_ok=True)

            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            image_path = os.path.join(upload_dir, f"captura_{timestamp}.jpg")

            with open(image_path, "wb") as file:
                file.write(response.content)

            print(f"✅ Imatge guardada a {image_path}")
            return jsonify({"missatge": "Captura feta!", "path": image_path})
        else:
            print("❌ Error HTTP:", response.status_code)
            return jsonify({"error": "No s'ha pogut capturar la imatge"}), 500

    except Exception as e:
        print("❌ Error de connexió:", e)
        return jsonify({"error": "No s'ha pogut connectar a la càmera"}), 500

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
