import requests
from datetime import datetime
import os

# IP del teu ESP32-CAM (canvia-ho si cal)
url_esp32 = 'http://192.168.1.55/capture'  # Modifica segons la IP real de l'ESP32-CAM

# Assegura't que la carpeta uploads existeix
os.makedirs("static/uploads", exist_ok=True)

# Obtenir la imatge
res = requests.get(url_esp32)

if res.status_code == 200:
    now = datetime.now().strftime('%Y%m%d_%H%M%S')
    nom_imatge = f'static/uploads/{now}_foto.jpg'

    with open(nom_imatge, 'wb') as f:
        f.write(res.content)

    print(f" Foto desada com: {nom_imatge}")
else:
    print(f" Error {res.status_code} en obtenir la imatge")
