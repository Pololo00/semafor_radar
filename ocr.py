import pytesseract
from PIL import Image
import cv2
import os

# Ruta de Tesseract per Windows
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Solapain\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

def detectar_matricula(nom_imatge):
    img = cv2.imread(nom_imatge)
    gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    temp_path = "temp.jpg"
    cv2.imwrite(temp_path, gris)

    text = pytesseract.image_to_string(Image.open(temp_path), config='--psm 8')
    os.remove(temp_path)

    return text.strip()
