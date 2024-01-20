import View.observer as observer

class Controller(observer.Observer):
    def __init__(self, req, view) -> None:
        self.request_handler = req
        self.view = view
        
        self.view.rent_book_listener(self.rent_book)
        self.view.return_book_listener(self.return_book)
        
    def start(self):
        self.view.run()

    def rent_book(self, user, book):
        #TODO get requests to db
        return "OK"

    def return_book(self, user, book):
        self.request_handler
        return "OK"
    
    def update(self, message):
        message_type, data = message

        match message_type:
            case "card":
                self.view.update_manager(data)
            case _:
                pass