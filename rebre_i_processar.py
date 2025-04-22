import easyocr
import cv2
import os

def processar_imatge(ruta_imatge):
    print(f"📥 Processant imatge: {ruta_imatge}")

    # Comprova que la imatge existeix
    if not os.path.exists(ruta_imatge):
        print("⚠️ La imatge no existeix!")
        return None

    # Inicialitza el lector EasyOCR
    lector = easyocr.Reader(['en'], gpu=False)  # Pots afegir 'es' si cal

    # Llegeix el text de la imatge
    resultats = lector.readtext(ruta_imatge)

    if not resultats:
        print("❌ No s'ha detectat text.")
        return None

    # Retorna només el text amb més confiança
    millor_resultat = max(resultats, key=lambda r: r[2])
    text_detectat = millor_resultat[1]
    confiança = millor_resultat[2]

    print(f"✅ Text detectat: {text_detectat} (confiança: {confiança:.2f})")
    return text_detectat
