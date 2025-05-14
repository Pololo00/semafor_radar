import easyocr
import cv2

# Crear lector EasyOCR
reader = easyocr.Reader(['en'], gpu=False)

# Ruta de la imatge
imatge_path = "static/uploads/captura_2025-05-13_20-00-15.jpg"
img = cv2.imread(imatge_path)

if img is None:
    print("⚠️ No s'ha pogut carregar la imatge. Comprova el camí.")
else:
    results = reader.readtext(img)

    if results:
        for (bbox, text, conf) in results:
            print(f"📛 Text detectat: {text} (confiança: {conf:.2f})")
    else:
        print("❌ No s'ha detectat cap text.")
