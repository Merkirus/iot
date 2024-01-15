from http.server import BaseHTTPRequestHandler
import socketserver
import cgi
import json

class Server(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'json')
        self.end_headers()

    def do_HEAD(self):
        self._set_headers()

    def do_GET(self):
        self._set_headers()
        form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'GET'}
            )
        data = {}
        self.wfile.write(str.encode(json.dumps(data)))

    def do_POST(self):
        self._set_headers()
        form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST'}
            )
        timestamp = form.getvalue('timestamp')
        uuid = form.getvalue('uuid')
        #TODO sth with database
        self.wfile.write(str.encode(f"TIMESTAMP: {timestamp}, UUID: {uuid}"))

if __name__ == "__main__":
    server_address = ("127.0.0.1", 8000)
    with socketserver.TCPServer(server_address, Server) as httpd:
        httpd.serve_forever()