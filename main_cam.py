# main_cam.py (MicroPython a ESP32-CAM)
from machine import Pin
import time
import network
import urequests

# Connexió WiFi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect("alumnes", "edu71243080")
while not wifi.isconnected():
    time.sleep(1)
print("Connectat! IP:", wifi.ifconfig()[0])

# Esperar senyal GPIO
sensor_pin = Pin(13, Pin.IN)

def fer_foto_i_enviar():
    print("📸 Capturant foto...")
    url = "http://192.168.1.100:5000/upload"  # Canvia pel teu Flask
    image_data = b"FAKE_IMAGE"  # Simulat

    headers = {"Content-Type": "image/jpeg"}
    res = urequests.post(url, data=image_data, headers=headers)
    print("Resposta del servidor:", res.text)

while True:
    if sensor_pin.value() == 1:
        fer_foto_i_enviar()
        time.sleep(2)  # Evita múltiples captures seguides
