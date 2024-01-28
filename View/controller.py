import View.observer as observer

class Controller(observer.Observer):
    def __init__(self, req, view) -> None:
        self.request_handler = req
        self.view = view
        
        self.view.rent_book_listener(self.rent_book)
        self.view.return_book_listener(self.return_book)
        self.view.login_listener(self.login)
        self.view.register_listener(self.register)
        self.view.insert_listener(self.insert_book)
        
    def start(self):
        self.view.run()

    def rent_book(self, user, book):
        return self.request_handler.post_rent(user, book)

    def return_book(self, user, book):
        return self.request_handler.post_return(user, book)
    
    def login(self, user, password):
        return self.request_handler.post_login(user, password)

    def register(self, uuid, name, surname, phone, email, password, role):
        print(uuid)
        return self.request_handler.post_register(uuid,
                                                  name,
                                                  surname,
                                                  phone,
                                                  email,
                                                  password,
                                                  role)
    
    def insert_book(self, author, title, isbn, id):
        return self.request_handler.post_book(author, title, isbn, id)
    
    def update(self, message):
        message_type, data = message
        print(f'data: ${data}')

        match message_type:
            case "card":
                self.view.update_card(data)
            case _:
                pass