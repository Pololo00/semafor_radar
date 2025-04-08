# sensor_velocitat.py (per a ESP32 amb HC-SR04)
from machine import Pin, time_pulse_us
import time

TRIG = Pin(5, Pin.OUT)  # Canvia segons els teus pins
ECHO = Pin(18, Pin.IN)
CAM_PIN = Pin(15, Pin.OUT)  # Pin que envia el senyal a la ESP32-CAM

VEL_LIMIT = 25  # límit en cm/s (ajusta segons el teu cas)

def obtenir_distancia():
    TRIG.off()
    time.sleep_us(2)
    TRIG.on()
    time.sleep_us(10)
    TRIG.off()

    duracio = time_pulse_us(ECHO, 1, 30000)
    distancia = duracio / 58.0  # en cm
    return distancia

# Loop principal
while True:
    d1 = obtenir_distancia()
    time.sleep(0.2)
    d2 = obtenir_distancia()

    velocitat = abs(d2 - d1) / 0.2  # cm/s
    print(f"Velocitat: {velocitat:.2f} cm/s")

    if velocitat > VEL_LIMIT:
        print("🚨 Excés de velocitat! Activant càmera.")
        CAM_PIN.on()
        time.sleep(0.5)
        CAM_PIN.off()
    else:
        print("Tot correcte.")
    
    time.sleep(1)
