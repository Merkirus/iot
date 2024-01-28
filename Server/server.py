from http.server import BaseHTTPRequestHandler
import socketserver
import cgi

import json

import Server.subject as subject
import Database.crud as crud
import Database.database as db
import Database.schemas as schemas
import datetime

from Database import database

DATE_FORMAT = "%Y-%m-%d"
session = database.SessionLocal()
class Server(socketserver.TCPServer, subject.Subject):

    def __init__(self, server_address):
        super().__init__(server_address, ServerHandler)
        subject.Subject.__init__(self)


class ServerHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def _set_headers_code(self,code):
        self.send_response(code)
        self.send_header('Content-type', 'json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_HEAD(self):
        self._set_headers()

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Credentials', 'true')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT')
        self.send_header("Access-Control-Allow-Headers", "*")
        self.end_headers()

    def do_GET(self):
        print(self.headers)
        print(self.rfile)
        form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'GET'}
            )
        
        path_arr = list(filter(None, self.path.split('/')))

        print(path_arr)

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
        elif len(path_arr) == 3:
            req_type = path_arr[0]
            req_id = path_arr[1]
            param = path_arr[2]
            match req_type:
                case 'user':
                    if crud.get_user_uid(session, int(req_id)) is not None and param == 'books':
                        books = crud.get_borrowed_by_user(session, int(req_id))
                        for book in books:
                            print(book.ReturnDate)
                        

                        response = list(map(lambda x: {'id': x.ID,
                                                       'borrowed': x.BorrowDate.strftime('%d-%m-%Y'),
                                                       'return_until': (x.BorrowDate+datetime.timedelta(days=14)).strftime('%d-%m-%Y'),
                                                       'days_left': ((x.BorrowDate+datetime.timedelta(days=14)) - datetime.date.today()).days,

                                                       # 'days_left': ((x.BorrowDate + datetime.timedelta(days=14)) - datetime.date(day=24,month=1, year=2024)).days,
                                                       'title': x.Book.Title.Title,
                                                       'author': x.Book.Title.Author

                                                       },books))
                        print(json.dumps(response))
                        self._set_headers()
                        self.wfile.write(str.encode(json.dumps(response)))
                        return

                case _:
                    pass
        elif len(path_arr) == 1:
            path_arr =  list(filter(None, path_arr[0].split('?')))
            print(path_arr[0])
            match path_arr[0]:
                case 'authenticate':
                    final_args = dict()
                    if len(path_arr) >= 2:
                        args = list(filter(None, path_arr[1].split('&')))
                        for arg in args :
                            print(arg)
                            splitted = list(filter(None, arg.split('=')))
                            print(splitted)
                            final_args[splitted[0]]=splitted[1]
                    else:
                        self._set_headers_code(403)
                        self.wfile.write(str.encode('Invalid params'))
                        return

                    print(final_args)

                    print('got form')
                    email = final_args['login']
                    password = final_args['password']
                    user = crud.get_user_email(session, email)

                    if user is None:
                        self._set_headers_code(404)
                        self.wfile.write(str.encode('Invalid credentials'))
                        return

                    if user.Password != password:
                        self._set_headers_code(410)
                        self.wfile.write(str.encode('Invalid credentials'))
                        return

                    response = {
                        'uid': user.UID
                    }
                    self._set_headers()
                    self.wfile.write(str.encode(json.dumps(response)))
                    return


        self.wfile.write(str.encode(self.path))


    def do_POST(self):
        print('start')
        print(self.headers)

        print(self.rfile)
        form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST'}
            )
        
        method = form.getvalue('_method')
        self._set_headers()
        response = ""

        match method:
            case 'card':
                uuid = form.getvalue('uuid')
                print(f'uid: {uuid}')
                if crud.get_user_uid(session, uuid):
                    response = "OK"
                else:
                    response = "Unknown user"
                self.server.notify_observers((method, uuid))
            case 'login':
                uuid = form.getvalue('login')
                password = form.getvalue('password')
                user = crud.get_user_uid(session, uuid)
                if user:
                    if user.Role != "worker":
                        response = "Client user"
                    elif user.Password == password:
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

                if uuid is None or name is None or surname is None or phone is None or email is None or password is None or role is None:
                    response = "All field are required"
                else:
                    crud.create_user(session, schemas.UserCreate(
                        UID=int(uuid),
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
                book = crud.get_book_by_id(session, book_id)
                if book:
                    user = crud.get_user_uid(session, uuid)
                    if user:
                        if crud.get_c_borrow_usr_book(session, uuid, book_id) != None:
                            response = "Book borrowed"
                        else:
                            crud.create_borrowed(session, schemas.CreateBorrowBook(
                                BorrowDate=datetime.date.today(),
                                ClientUID=uuid,
                                BookID=book_id
                            ))
                            response = "OK"
                    else:
                        response = "User unknown"
                else:
                    response = "Book unknown"
            case 'return':
                uuid = form.getvalue('uuid')
                book_id = form.getvalue('book')
                book = crud.get_book_by_id(session, book_id)
                if book:
                    user = crud.get_user_uid(session, uuid)
                    if user:
                        borrowed_book = crud.get_c_borrow_usr_book(session, uuid, book_id)
                        if borrowed_book:
                            borrowed_book.ReturnDate = datetime.date.today()
                            crud.save_borrowed(session,borrowed_book)
                            response = "OK"
                            
                        else:
                            response = "Book not rented"
                    else:
                        response = "User unknown"
                else:
                    response = "Book unknown"

            case 'insert':
                author = form.getvalue('author')
                title = form.getvalue('title')
                isbn = form.getvalue('isbn')
                id = form.getvalue("id")
                if author is None or title is None or isbn is None or id is None:
                    response = 'All fields are required'
                    self.wfile.write(str.encode(response))
                    return

                if crud.get_book_by_id(session,id) is not None:
                    response = 'Book with given id already exists'
                    self.wfile.write(str.encode(response))
                    return



                title_instance = crud.get_title_by_isbn(db.SessionLocal(), isbn)

                if title_instance == None:
                    crud.create_title(session, schemas.TitleCreate(
                        ISBN=isbn,
                        Author=author,
                        Title=title
                    ))

                crud.create_book(session, schemas.BookCreate(
                    ISBN=isbn,
                    id=id
                ))
                response = "OK"


            case _:
                self.wfile.write(str.encode("UNKNOWN"))

        self.wfile.write(str.encode(response))






if __name__ == "__main__":
    server_address = ("127.0.0.1", 8000)
    with socketserver.TCPServer(server_address, ServerHandler) as httpd:
        httpd.serve_forever()