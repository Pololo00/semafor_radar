from machine import Pin, time_pulse_us 
import time
import network
import red
import requests

VEL_LIMIT = 50  # cm/s
CAM_IP = "http://172.16.5.195/"  # Sustituye por la IP real de la ESP32-CAM
# Configuración de los pines del sensor HC-SR04
TRIG = Pin(5, Pin.OUT)  # Pin de Trigger
ECHO = Pin(18, Pin.IN)  # Pin de Echo

red.do_connect("Alumnes","edu71243080")

def obtener_distancia():
    TRIG.off()  # Asegurarse que el Trigger esté apagado
    time.sleep_us(2)  # Breve espera
    TRIG.on()  # Enviar pulso ultrasónico
    time.sleep_us(10)  # Pulso de 10 microsegundos
    TRIG.off()  # Apagar el Trigger

    # Medir el tiempo que tarda el eco en regresar
    duracion = time_pulse_us(ECHO, 1, 30000)  # Medir duración en microsegundos
    if duracion < 0:
        return -1  # Si no se recibe la señal de vuelta, devolver -1 (error)
    
    distancia = duracion / 58.0  # Convertir la duración a distancia en cm (velocidad del sonido)
    return distancia


intervalo = 1  # 200 ms entre mediciones (ajustar según necesidad)

# Bucle principal para medir velocidad
while True:
    # Obtener la distancia en el primer tiempo
    distancia1 = obtener_distancia()
    time.sleep(intervalo)

    # Obtener la distancia en el segundo tiempo
    distancia2 = obtener_distancia()

    # Calcular la velocidad (cambio de distancia / tiempo)
    velocidad = abs(distancia2 - distancia1) / intervalo  # cm/s

    print(f"Distancia 1: {distancia1:.2f} cm")
    print(f"Distancia 2: {distancia2:.2f} cm")
    print(f"Velocidad: {velocidad:.2f} cm/s")
    
    if velocidad > VEL_LIMIT:
        print('salta el radar')
        # La URL del servidor Flask donde se va a realizar la solicitud GET
        url = "http://127.0.0.1:5000//activar_radar"

        # Realiza la solicitud GET y guarda la respuesta
        response = requests.get(url)

        # Comprueba si la solicitud fue exitosa
        if response.status_code == 200:
            print("Respuesta del servidor:", response.json())  # Imprime la respuesta en formato JSON
        else:
            print("Error en la solicitud:", response.status_code)

    time.sleep(1)  # Esperar antes de la siguiente medición
