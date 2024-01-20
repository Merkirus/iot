import Server.server as server
import View.controller as controller
import View.view as view
import Server.request_handler as request_handler
import threading
from Database import models, database

models.Base.metadata.create_all(bind=database.engine)

def start():
    req = request_handler.RequestHandler("http://localhost:8000")
    vi = view.Gui()
    con = controller.Controller(req, vi)
    serv = server.Server(("127.0.0.1", 8000))
    serv.add_observer(con)
    server_thread = threading.Thread(target=lambda: start_server(serv))
    server_thread.start()
    con.start()
    server_thread.join()

def start_server(server):
    with server as httpd:
        httpd.serve_forever()

if __name__ == "__main__":
    start()