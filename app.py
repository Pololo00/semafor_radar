from flask import Flask, request, jsonify
import os
from datetime import datetime

esp32_ip = "http://172.16.3.220/capture"  # IP actual de la càmera

app = Flask(__name__)

# Carpeta per emmagatzemar les imatges
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ruta per rebre la foto de l'ESP32
@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return "No hi ha cap fitxer a la petició", 400

    file = request.files['file']
    if file.filename == '':
        return "No s'ha seleccionat cap fitxer", 400

    # Obtenir la data actual per desar la imatge
    now = datetime.now().strftime('%Y%m%d_%H%M%S')
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{now}_foto.jpg")
    
    # Desa la imatge a la carpeta static/uploads/
    file.save(filepath)
    print(f"Imatge desada a {filepath}")
    
    # Ara cridem la funció d'OCR per processar la matrícula
    matricula = detectar_matricula(filepath)
    
    return jsonify({'message': 'Imatge processada correctament', 'matricula': matricula})

def save_user(username, password, email=None):
    hashed_password = generate_password_hash(password)  # Encriptar la contraseña
    cursor = conn.cursor()
    try:
        cursor.execute(
            'INSERT INTO users (username, password, email) VALUES (%s, %s, %s)',
            (username, hashed_password, email)
        )
        conn.commit()
    except mysql.connector.IntegrityError:
        return "El usuario o el correo ya existen"
    finally:
        cursor.close()

def get_users():
    cursor = conn.cursor()
    cursor.execute('SELECT id, username, email, created_at FROM users')
    users = cursor.fetchall()
    cursor.close()
    return users

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)      hola pola
