# main_micro.py (Control del sensor HC-SR04 i càmera ESP32)
from machine import Pin
import time
import network
import urequests

# Configura WiFi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect("alumnes", "edu71243080")
while not wifi.isconnected():
    time.sleep(1)
print("Connectat a la xarxa WiFi! IP:", wifi.ifconfig()[0])

# Configura el pin per l'HC-SR04
TRIG = Pin(5, Pin.OUT)  # Pin de Trigger
ECHO = Pin(18, Pin.IN)  # Pin de Echo
CAM_PIN = Pin(15, Pin.OUT)  # Pin de la càmera ESP32

VEL_LIMIT = 25  # Límite de velocitat en cm/s

def obtenir_distancia():
    TRIG.off()
    time.sleep_us(2)
    TRIG.on()
    time.sleep_us(10)
    TRIG.off()

    duracio = time_pulse_us(ECHO, 1, 30000)
    distancia = duracio / 58.0  # en cm
    return distancia

# Funció per activar la càmera
def activar_camera():
    url = "http://192.168.1.100:5000/upload"  # URL del teu servidor Flask
    image_data = b"FAKE_IMAGE"  # Això ha de ser la imatge real

    headers = {"Content-Type": "image/jpeg"}
    res = urequests.post(url, data=image_data, headers=headers)
    print("Resposta del servidor:", res.text)

# Bucle principal
while True:
    d1 = obtenir_distancia()
    time.sleep(0.2)
    d2 = obtenir_distancia()

    velocitat = abs(d2 - d1) / 0.2  # cm/s
    print(f"Velocitat: {velocitat:.2f} cm/s")

    if velocitat > VEL_LIMIT:
        print("🚨 Velocitat massa alta! Activant càmera...")
        CAM_PIN.on()
        time.sleep(0.5)  # Activa la càmera breument
        CAM_PIN.off()
        activar_camera()  # Envia la foto
    else:
        print("Tot correcte.")

    time.sleep(1)
