import React, { useState } from "react";
import axios from "axios";

const FileUpload = () => {
    const [file, setFile] = useState(null);
    const [message, setMessage] = useState("");

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const handleUpload = async () => {
        if (!file) {
            setMessage("Por favor, selecciona un archivo.");
            return;
        }

        const formData = new FormData();
        formData.append("file", file);

        try {
            const response = await axios.post("http://127.0.0.1:5000/process", formData, {
                responseType: "blob", // Para manejar archivos como respuesta
            });

            // Descargar el archivo
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement("a");
            link.href = url;
            link.setAttribute("download", "resultados.xlsx");
            document.body.appendChild(link);
            link.click();

            setMessage("Archivo procesado con éxito.");
        } catch (error) {
            setMessage("Error procesando el archivo.");
            console.error(error);
        }
    };

    return (
        <div>
            <h2>Subir Archivo</h2>
            <input type="file" onChange={handleFileChange} />
            <button onClick={handleUpload}>Subir y Procesar</button>
            {message && <p>{message}</p>}
        </div>
    );
};

export default FileUpload;
