from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse as urlparse

class SimpleIAHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse.urlparse(self.path)
        if parsed.path != "/investigar":
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Ruta no encontrada.")
            return

        query = urlparse.parse_qs(parsed.query)
        tema = query.get("tema", [None])[0]

        if not tema:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Falta el parametro 'tema'")
            return

        # Aquí importamos lo necesario
        from vaal.buscador import buscar_en_duckduckgo
        from vaal.lector import extraer_texto_de_url
        from vaal.analizador import analizar_con_pregunta
        from vaal.personalidad import dar_estilo

        try:
            links = buscar_en_duckduckgo(tema)
            textos = [extraer_texto_de_url(link) for link in links]
            texto_completo = "\n\n".join(textos)
            respuesta = analizar_con_pregunta(texto_completo, f"¿Qué se puede decir sobre {tema}?")
            respuesta_final = dar_estilo(respuesta, tono="profesional", firma=True)

            self.send_response(200)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(respuesta_final.encode('utf-8'))

        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"Error interno: {str(e)}".encode())

# Lanzar el servidor
if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 8000), SimpleIAHandler)
    print("Servidor corriendo en http://localhost:8000")
    server.serve_forever()
