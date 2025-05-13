from flask import Flask, jsonify
import os
import requests
from datetime import datetime
from ocr import detectar_matricula  # ✅ Importar la funció OCR

esp32_ip = "http://172.16.3.220/capture"  # IP actual de la càmera

app = Flask(__name__)

lectures_matricula = []  # ✅ Array per guardar les dades llegides

@app.route('/activar_radar', methods=['GET'])
def activar_radar():
    print("📡 Radar activat")

    try:
        response = requests.get(esp32_ip, timeout=5)

        if response.status_code == 200:
            upload_dir = "static/uploads"
            os.makedirs(upload_dir, exist_ok=True)

            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            image_filename = f"captura_{timestamp}.jpg"
            image_path = os.path.join(upload_dir, image_filename)

            with open(image_path, "wb") as file:
                file.write(response.content)

            print(f"✅ Imatge guardada a {image_path}")

            # 🧠 Executar OCR
            matricula = detectar_matricula(image_path)
            print(f"🔍 Matrícula detectada: {matricula}")

            # ✅ Guardar la dada en l’array
            lectures_matricula.append({
                "timestamp": timestamp,
                "imatge": image_filename,
                "matricula": matricula
            })

            return jsonify({
                "missatge": "Captura feta!",
                "imatge": image_filename,
                "matricula": matricula
            })

        else:
            print("❌ Error HTTP:", response.status_code)
            return jsonify({"error": "No s'ha pogut capturar la imatge"}), 500

    except Exception as e:
        print("❌ Error de connexió:", e)
        return jsonify({"error": "No s'ha pogut connectar a la càmera"}), 500

# Endpoint per consultar les lectures registrades
@app.route('/lectures', methods=['GET'])
def obtenir_lectures():
    return jsonify(lectures_matricula)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
