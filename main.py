# main.py
from flask import Flask, request, send_from_directory
import os
from ocr import detectar_matricula

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/static/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return 'No s\'ha trobat cap imatge', 400

    file = request.files['image']
    if file.filename == '':
        return 'Nom d\'arxiu buit', 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    text = detectar_matricula(filepath)
    return f"Matrícula detectada: {text}", 200

if __name__ == '__main__':
    app.run(debug=True)
