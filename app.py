from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)
CORS(app)  # Permite solicitudes desde React
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Crea la carpeta si no existe

@app.route('/process', methods=['POST'])
def process_file():
    try:
        # Validar si se subió un archivo
        if 'file' not in request.files:
            return jsonify({"message": "No se envió ningún archivo"}), 400

        file = request.files['file']
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        # Leer el archivo Excel con pandas
        df = pd.read_excel(filepath)

        # Procesar el archivo (ejemplo: sumar valores por columna)
        processed = df.sum(numeric_only=True).reset_index()
        processed.columns = ['Columna', 'Suma']

        # Guardar el resultado en un nuevo archivo Excel
        output_path = os.path.join(UPLOAD_FOLDER, "resultados.xlsx")
        processed.to_excel(output_path, index=False)

        # Devolver el archivo procesado al cliente
        return send_file(output_path, as_attachment=True)

    except Exception as e:
        return jsonify({"message": f"Error procesando el archivo: {str(e)}"}), 500


@app.route('/')
def home():
    return "¡Servidor Flask funcionando! Usa el endpoint /process para procesar archivos."


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
