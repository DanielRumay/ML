# main.py

from http.server import HTTPServer
from api.endpoints import APIHandler

def run(server_class=HTTPServer, handler_class=APIHandler, port=8000):
    server_address = ("0.0.0.0", port)
    httpd = server_class(server_address, handler_class)
    print(f"Servidor iniciado en el puerto {port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run()