# ocr.py
import easyocr
import os

lector = easyocr.Reader(['en'], gpu=False)

def detectar_matricula(ruta_imatge):
    if not os.path.exists(ruta_imatge):
        return "⚠️ Imatge no trobada"

    resultats = lector.readtext(ruta_imatge)

    if not resultats:
        return "❌ No s'ha detectat cap text"

    millor = max(resultats, key=lambda r: r[2])  # r[2] = confiança
    return millor[1]
