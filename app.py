from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector

# Configuración de la conexión a la base de datos MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Asdqwe!23",
    database="semafor"
)

esp32_ip = "http://172.16.3.220/capture"  # IP actual de la càmera

app = Flask(__name__)
app.secret_key = 'secret_key'  # Clave secreta para las sesiones

# Carpeta para almacenar las imágenes
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ruta para recibir la foto del ESP32
@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return "No hi ha cap fitxer a la petició", 400

    file = request.files['file']
    if file.filename == '':
        return "No s'ha seleccionat cap fitxer", 400

    # Obtener la fecha actual para guardar la imagen
    now = datetime.now().strftime('%Y%m%d_%H%M%S')
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{now}_foto.jpg")
    
    # Guardar la imagen en la carpeta static/uploads/
    file.save(filepath)
    print(f"Imatge desada a {filepath}")
    
    # Aquí puedes llamar a la función de OCR para procesar la matrícula
    matricula = detectar_matricula(filepath)  # Asegúrate de que esta función esté definida
    
    return jsonify({'message': 'Imatge processada correctament', 'matricula': matricula})

# Función para guardar un usuario en la base de datos
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

# Función para validar un usuario al iniciar sesión
def validate_user(username, password):
    cursor = conn.cursor()
    cursor.execute('SELECT password FROM users WHERE username = %s', (username,))
    user = cursor.fetchone()
    cursor.close()

    if user and check_password_hash(user[0], password):
        return True
    return False

# Función para obtener todos los usuarios
def get_users():
    cursor = conn.cursor()
    cursor.execute('SELECT id, username, email, created_at FROM users')
    users = cursor.fetchall()
    cursor.close()
    return users

# Ruta para registrar usuarios
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')

        result = save_user(username, password, email)
        if result == "El usuario o el correo ya existen":
            return result, 400

        return redirect(url_for('login'))  # Redirigir al login después del registro

    return render_template('register.html')

# Ruta para iniciar sesión
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if validate_user(username, password):
            session['user'] = username  # Guardar usuario en la sesión
            return redirect(url_for('registres'))
        else:
            return "Credenciales incorrectas", 401

    return render_template('login.html')

# Ruta para mostrar los registros de multas
@app.route('/registres')
def registres():
    if 'user' not in session:
        return redirect(url_for('login'))  # Redirigir al login si no está autenticado

    cursor = conn.cursor()
    cursor.execute('SELECT matricula, velocitat, imatge_path, processat_ocr FROM semafor')
    dades = cursor.fetchall()
    cursor.close()

    return render_template('registres.html', dades=dades)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
