from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import os
import requests
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from ocr import detectar_matricula  # ✅ Importar la funció OCR
from functools import wraps

# Configuración de la conexión a la base de datos MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="semafor"
)

app = Flask(__name__)
app.secret_key = 'secret_key'  # Clave secreta para las sesiones

# Carpeta para almacenar las imágenes
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Configuración de la conexión a la base de datos MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="semafor"
)
app = Flask(__name__)
app.secret_key = 'secret_key'  # Clave secreta para las sesiones

# Carpeta para almacenar las imágenes
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

esp32_ip = "http://172.16.1.215/capture"  # IP actual de la càmera

lectures_matricula = []  # ✅ Array per guardar les dades llegides

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:  # Verifica si el usuario está en la sesión
            return redirect(url_for('login'))  # Redirige al login si no está autenticado
        return f(*args, **kwargs)
    return decorated_function

@app.route('/activar_radar', methods=['GET'])
def activar_radar():
    print("📡 Radar activat")
    velocitat = request.args.get('velocitat', type=float)
    print(f"🚗 Velocitat rebuda: {velocitat}")
    try:
        response = requests.get(esp32_ip, timeout=5)

        if response.status_code == 200:
            timestamp_obj = datetime.now()
            timestamp_str = timestamp_obj.strftime("%Y-%m-%d_%H-%M-%S")
            image_filename = f"captura_{timestamp_str}.jpg"
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)

            # Guardar la imatge
            with open(image_path, "wb") as file:
                file.write(response.content)
            print(f"✅ Imatge guardada a {image_path}")

            # OCR
            matricula = detectar_matricula(image_path)
            print(f"🔍 Matrícula detectada: {matricula}")

            if not matricula:  # Si no detecta res
                print("⚠️ No s'ha detectat cap matrícula. No es guarda a la base de dades.")
                return jsonify({
                    "missatge": "No s'ha detectat matrícula.",
                    "imatge": image_filename,
                    "matricula": None
                }), 200

            # Simular velocitat (o agafa-la realment)
            velocitat = velocitat if velocitat else 80.5

            # Guardar en array (opcional)
            lectures_matricula.append({
                "timestamp": timestamp_str,
                "imatge": image_filename,
                "matricula": matricula,
                "velocitat": velocitat
            })

            # Insertar a la base de dades amb timestamp
            cursor = conn.cursor()
            try:
                cursor.execute(
                    'INSERT INTO radar_deteccions (matricula, velocitat, imatge_path, processat_ocr, timestamp) VALUES (%s, %s, %s, %s, %s)',
                    (matricula, velocitat, image_path, True, timestamp_obj.strftime('%Y-%m-%d %H:%M:%S'))
                )
                conn.commit()
                print("✅ Dades inserides a la base de dades")
            except mysql.connector.Error as err:
                print(f"❌ Error al inserir dades: {err}")
            finally:
                cursor.close()

            return jsonify({
                "missatge": "Captura feta!",
                "imatge": image_filename,
                "matricula": matricula,
                "velocitat": velocitat
            })

        else:
            print("❌ Error de connexió amb la càmera")
            return jsonify({"error": "No s'ha pogut connectar a la càmera"}), 500
    except Exception as e:
        print("❌ Error de connexió:", e)
        return jsonify({"error": "No s'ha pogut connectar a la càmera"}), 500


# Endpoint per consultar les lectures registrades
@app.route('/lectures', methods=['GET'])
def obtenir_lectures():
    return jsonify(lectures_matricula)
#prueba
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

    # Simular la velocidad (puedes reemplazar esto con un cálculo real si lo tienes)
    velocitat = 80.5  # Velocidad simulada, reemplázala con el valor real

    # Insertar los datos en la tabla radar_deteccions
    timestamp_db = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

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


# 👇 AFEGEIX AIXÒ ABANS de la ruta /register
def save_user(username, password, email=None):
    hashed_password = generate_password_hash(password)  # Encripta la contrasenya
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

# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    session.pop('user', None)  # Elimina el usuario de la sesión
    return redirect(url_for('login'))  # Redirige al login

# Ruta para mostrar los registros de multas
@app.route('/registres')
@login_required
def registres():
    if 'user' not in session:
        return redirect(url_for('login'))  # Redirigir al login si no está autenticado

    cursor = conn.cursor()
    cursor.execute('SELECT matricula, velocitat, imatge_path, processat_ocr, timestamp FROM radar_deteccions')
    dades = cursor.fetchall()
    cursor.close()

    return render_template('registres.html', dades=dades)

# Ruta para recibir la foto del ESP32

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
