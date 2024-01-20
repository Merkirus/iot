from http.server import BaseHTTPRequestHandler
import socketserver
import cgi
import Server.subject as subject

class Server(socketserver.TCPServer, subject.Subject):
    def __init__(self, server_address):
        super().__init__(server_address, ServerHandler)
        subject.Subject.__init__(self)

class ServerHandler(BaseHTTPRequestHandler):
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
        
        path_arr = list(filter(None, self.path.split('/')))

        if len(path_arr) == 2:
            req_type = path_arr[0]
            req_id = path_arr[1]

        self.wfile.write(str.encode(self.path))

    def do_POST(self):
        self._set_headers()
        form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST'}
            )
        
        method = form.getvalue('_method')

        match method:
            case 'card':
                uuid = form.getvalue('uuid')
                #TODO sth with database
                self.server.notify_observers((method, uuid))
                self.wfile.write(str.encode("OK"))
            case _:
                self.wfile.write(str.encode("UNKNOWN"))
        

if __name__ == "__main__":
    server_address = ("127.0.0.1", 8000)
    with socketserver.TCPServer(server_address, ServerHandler) as httpd:
        httpd.serve_forever()