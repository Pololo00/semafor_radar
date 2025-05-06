import requests

# IP del ESP32 (Asegúrate de cambiar esta dirección por la IP correcta del ESP32)
esp32_ip = "http://172.16.6.150/capture"

# Hacer la solicitud HTTP GET al ESP32 para capturar la imagen
response = requests.get(esp32_ip)

# Verificar si la solicitud fue exitosa
if response.status_code == 200:
    # Guardar la imagen en el disco duro
    with open("captura.jpg", "wb") as file:
        file.write(response.content)
    print("✅ Imagen guardada en captura.jpg")
else:
    print("❌ Error al obtener la imagen:", response.status_code)
