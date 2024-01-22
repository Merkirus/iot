from http.server import BaseHTTPRequestHandler
import socketserver
import cgi
import Server.subject as subject
import Database.crud as crud
import Database.database as db
import Database.schemas as schemas
import datetime

DATE_FORMAT = "%Y-%m-%d"

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
            match req_type:
                case 'user':
                    pass
                case 'book':
                    pass
                case _:
                    pass

        self.wfile.write(str.encode(self.path))

    def do_POST(self):
        self._set_headers()
        form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST'}
            )
        
        method = form.getvalue('_method')

        response = ""

        match method:
            case 'card':
                uuid = form.getvalue('uuid')
                if crud.get_user_uid(db.SessionLocal(), uuid):
                    response = "OK"
                else:
                    response = "Unknown user"
                self.server.notify_observers((method, uuid))
            case 'login':
                uuid = form.getvalue('login')
                password = form.getvalue('password')
                user = crud.get_user_uid(db.SessionLocal(), uuid)
                if user:
                    if user.Password == password:
                        response = "OK"
                    else:
                        response = "Wrong password"
                else:
                    response = "Unknown user"
            case 'register':
                uuid = form.getvalue('uuid')
                name = form.getvalue('name')
                surname = form.getvalue('surname')
                phone = form.getvalue('phone')
                email = form.getvalue('email')
                password = form.getvalue('password')
                role = form.getvalue('role')
                crud.create_user(db.SessionLocal(), schemas.UserCreate(
                    UID=uuid,
                    Name=name,
                    LastName=surname,
                    Phone=phone,
                    Email=email,
                    Password=password,
                    Role=role
                ))
                response = "OK"
            case 'rent':
                uuid = form.getvalue('uuid')
                book_id = form.getvalue('book')
                book = crud.get_book_by_id(db.SessionLocal(), book_id)
                if book:
                    user = crud.get_user_uid(db.SessionLocal(), uuid)
                    if user:
                        crud.create_borrowed(db.SessionLocal(), schemas.CreateBorrowBook(
                            BorrowDate=datetime.datetime.now(),
                            ClientUID=uuid,
                            BookId=book_id
                        ))
                    else:
                        response = "User unknown"
                else:
                    response = "Book unknown"
                response = "OK"
            case 'return':
                uuid = form.getvalue('uuid')
                book_id = form.getvalue('book')
                book = crud.get_book_by_id(db.SessionLocal(), book_id)
                if book:
                    user = crud.get_user_uid(db.SessionLocal(), uuid)
                    if user:
                        borrowed_book = crud.get_c_borrow_usr_book(db.SessionLocal(), uuid, book_id)
                        if borrowed_book:
                            borrowed_book.ReturnDate = datetime.datetime.now()
                        else:
                            response = "Book not rented"
                    else:
                        response = "User unknown"
                else:
                    response = "Book unknown"
                response = "OK"
            case 'insert':
                author = form.getvalue('author')
                title = form.getvalue('title')
                isbn = form.getvalue('isbn')
                title_instance = crud.get_title_by_isbn(db.SessionLocal(), isbn)
                if title_instance == None:
                    crud.create_title(db.SessionLocal(), schemas.TitleCreate(
                        ISBN=isbn,
                        Author=author,
                        Title=title
                    ))
                    title_instance = crud.get_title_by_isbn(db.SessionLocal(), isbn)
                crud.create_book(db.SessionLocal(), schemas.BookCreate(
                    ISBN=isbn
                ))
                response = "OK"
            case _:
                self.wfile.write(str.encode("UNKNOWN"))

        self.wfile.write(str.encode(response))
        

if __name__ == "__main__":
    server_address = ("127.0.0.1", 8000)
    with socketserver.TCPServer(server_address, ServerHandler) as httpd:
        httpd.serve_forever()