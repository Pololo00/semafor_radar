from machine import Pin
import time
import network
import urequests
import camera  # Per a la càmera ESP32

# Connexió WiFi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect("alumnes", "edu71243080")
while not wifi.isconnected():
    time.sleep(1)
print("Connectat a WiFi! IP:", wifi.ifconfig()[0])

# Configuració dels pins per al sensor HC-SR04
TRIG = Pin(5, Pin.OUT)  # Pin de Trigger
ECHO = Pin(18, Pin.IN)  # Pin de Echo
CAM_PIN = Pin(15, Pin.OUT)  # Pin de la càmera ESP32 (pot variar depenent de la teva configuració)

VEL_LIMIT = 25  # Límite de velocitat en cm/s (ajusta a les teves necessitats)

# Configuració de la càmera ESP32
camera.init(0, format=camera.JPEG)  # Inicia la càmera amb format JPEG

# Funció per obtenir la distància
def obtenir_distancia():
    TRIG.off()
    time.sleep_us(2)
    TRIG.on()
    time.sleep_us(10)
    TRIG.off()

    duracio = time_pulse_us(ECHO, 1, 30000)
    distancia = duracio / 58.0  # en cm
    return distancia

# Funció per activar la càmera i enviar la imatge al servidor Flask
def activar_camera():
    print("📸 Capturant foto...")

    # Captura la imatge de la càmera ESP32
    buf = camera.capture()  # Captura la imatge en format JPEG

    # Envia la imatge al servidor Flask
    url = "http://192.168.1.100:5000/upload"  # URL del servidor Flask (ajusta si cal)
    headers = {"Content-Type": "image/jpeg"}
    res = urequests.post(url, data=buf, headers=headers)
    
    print("Resposta del servidor:", res.text)

# Bucle principal per controlar el sensor i activar la càmera
while True:
    d1 = obtenir_distancia()
    time.sleep(0.2)
    d2 = obtenir_distancia()

    # Calcular la velocitat del vehicle
    velocitat = abs(d2 - d1) / 0.2  # cm/s
    print(f"Velocitat: {velocitat:.2f} cm/s")

    if velocitat > VEL_LIMIT:
        print("🚨 Velocitat massa alta! Activant càmera...")
        CAM_PIN.on()
        time.sleep(0.5)  # Activa la càmera breument
        CAM_PIN.off()
        activar_camera()  # Envia la foto
    else:
        print("Tot correcte. El vehicle no va massa ràpid.")

    time.sleep(1)  # Espera 1 segon abans de tornar a llegir la distància
