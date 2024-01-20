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

    def post_card(self, params):
        uuid = params

        response = requests.post(self.url, data={'uuid': uuid, '_method': 'card'})

        return response.text

if __name__ == "__main__":
    request = RequestHandler("http://localhost:8000")
    print(request.post_card("123"))