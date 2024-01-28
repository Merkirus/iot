import requests

class RequestHandler():
    def __init__(self, url) -> None:
        super().__init__()
        self.url = url

    def get_user(self, uuid):
        response = requests.get(f"{self.url}/user/{uuid}")

        return response.text
    
    def get_book(self, book):
        response = requests.get(f"{self.url}/book/{book}")

        return response.text
    
    def post_rent(self, user, book):
        method = 'rent'

        response = requests.post(self.url, data={'uuid': user,
                                                 'book': book,
                                                 "_method": method})
        
        return response.text
    
    def post_return(self, user, book):
        method = 'return'

        response = requests.post(self.url, data={'uuid': user,
                                                 'book': book,
                                                 "_method": method})
        
        return response.text

    def post_card(self, uuid):
        method = 'card'

        response = requests.post(self.url, data={'uuid': uuid, '_method': method})

        return response.text

    def post_book(self, author, title, isbn, id):
        method = 'insert'

        response = requests.post(self.url, data={'author': author,
                                                 "title": title,
                                                 "isbn": isbn,
                                                 "id":id,
                                                 "_method": method})

        return response.text
    
    def post_login(self, login, password):
        method = 'login'

        #For better security hash should be added
        response = requests.post(self.url, data={'login': login, 'password': password, '_method': method})

        return response.text
    
    def post_register(self, uuid, name, surname, phone, email, password, role):
        method = 'register'

        #For better security hash should be added
        response = requests.post(self.url, data={"uuid": uuid,
                                                 "name": name,
                                                 "surname": surname,
                                                 "phone": phone,
                                                 "email": email,
                                                 "password": password,
                                                 "role": role,
                                                 "_method": method})

        return response.text

if __name__ == "__main__":
    request = RequestHandler("http://localhost:8000")
    print(request.post_card("123"))