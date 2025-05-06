UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return jsonify({"error": "No image part"}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # Carregar la imatge i fer OCR
    img = cv2.imread(filepath)
    results = reader.readtext(img)

    # Si es detecta alguna matrícula
    if results:
        texts = [text for (_, text, _) in results]
        return jsonify({"matricula_detectada": texts}), 200
    else:
        return jsonify({"error": "No es detecta cap matrícula"}), 400