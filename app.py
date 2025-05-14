from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import os
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from ocr import detectar_matricula

app = Flask(__name__)
app.secret_key = 'secret_key'  # Clave secreta para las sesiones

import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Asdqwe!23",
    database="semafor"
)
# Configuración de la carpeta de imágenes
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ruta para la página de login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Validar credenciales desde la base de datos
        if validate_user(username, password):
            session['user'] = username  # Guardar usuario en la sesión
            return redirect(url_for('registres'))
        else:
            return "Credenciales incorrectas", 401

    return render_template('login.html')

# Ruta para la página de registro
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

# Función para validar usuario y contraseña
def validate_user(username, password):
    cursor = conn.cursor()
    cursor.execute('SELECT password FROM users WHERE username = %s', (username,))
    user = cursor.fetchone()
    cursor.close()

    if user and check_password_hash(user[0], password):
        return True
    return False

# Ruta para el registro de multas (protegida)
@app.route('/registres')
def registres():
    if 'user' not in session:
        return redirect(url_for('login'))  # Redirigir al login si no está autenticado

    # Obtener los datos de la tabla `semafor`
    cursor = conn.cursor()
    cursor.execute('SELECT matricula, velocitat, imatge_path, processat_ocr FROM radar_deteccions')
    dades = cursor.fetchall()
    cursor.close()

    # Pasar los datos a la plantilla
    return render_template('registres.html', dades=dades)

# Ruta para mostrar todos los usuarios
@app.route('/users')
def users():
    if 'user' not in session:
        return redirect(url_for('login'))  # Redirigir al login si no está autenticado

    users = get_users()  # Obtener los usuarios de la base de datos
    return render_template('users.html', users=users)

# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    session.pop('user', None)  # Eliminar usuario de la sesión
    return redirect(url_for('login'))

# Ruta para recibir la foto del ESP32
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
    app.run(host='0.0.0.0', port=5000, debug=True)
