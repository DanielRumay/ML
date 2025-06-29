from http.server import BaseHTTPRequestHandler
from db.connection import get_mongo_collection
from processing.random_forest_model import train_random_forest
from recomendation.logic import get_recommendations
import json

class APIHandler(BaseHTTPRequestHandler):
    def _set_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")  # Para permitir cualquier origen
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")


    def _send_response(self, status_code, data=None):
        """
        Método común para enviar respuestas con encabezados CORS.
        """
        self.send_response(status_code)
        self._set_cors_headers()
        self.send_header("Content-type", "application/json")
        self.end_headers()

        if data:
            self.wfile.write(json.dumps(data).encode())

    def do_OPTIONS(self):
        """
        Manejo de solicitudes OPTIONS (preflight CORS).
        """
        self.send_response(200)
        self._set_cors_headers()
        self.end_headers()

    def do_POST(self):
        """
        Manejo de solicitudes POST para /train y /recommendations.
        """
        if self.path == "/train":
            try:
                # Obtener datos de MongoDB
                collection = get_mongo_collection("movies")
                data = list(collection.find({}, {"_id": 0}))

                # Entrenar modelo
                train_random_forest(data)
                self._send_response(200, {"message": "Modelo entrenado exitosamente"})

            except Exception as e:
                self._send_response(500, {"error": f"Error al entrenar el modelo: {str(e)}"})

        elif self.path == "/recommendations":
            try:
                content_length = int(self.headers["Content-Length"])
                post_data = self.rfile.read(content_length)
                request_data = json.loads(post_data)
                title = request_data.get("title")

                if not title:
                    self._send_response(400, {"error": "Falta el título de la película"})
                    return

                # Obtener datos y recomendaciones
                collection = get_mongo_collection("movies")
                data = list(collection.find({}, {"_id": 0}))
                recommendations = get_recommendations(title, 5, data)

                self._send_response(200, recommendations)

            except Exception as e:
                self._send_response(500, {"error": f"Error interno del servidor: {str(e)}"})

        else:
            self._send_response(404, {"error": "Endpoint no encontrado"})
