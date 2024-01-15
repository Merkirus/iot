from io import BytesIO
import pycurl
import json

class Request():
    def __init__(self, url) -> None:
        self.url = url
        pass

    # TODO
    def get_json(self, params):
        respone = BytesIO()

        c = pycurl.Curl()
        c.setopt(pycurl.URL, self.url)
        c.setopt(pycurl.WRITEDATA, respone)
        try:
            c.perform()
        except:
            return "Can not connect to server"

        c.close()

        return respone.getvalue().decode()

    def post_json(self, params):
        timestamp, uuid = params

        data = f'timestamp={timestamp}&uuid={uuid}'

        respone = BytesIO()

        c = pycurl.Curl()
        c.setopt(pycurl.URL, self.url)
        c.setopt(pycurl.POSTFIELDS, data)
        c.setopt(pycurl.WRITEFUNCTION, respone.write)
        try:
            c.perform()
        except:
            return "Can not connect to server"

        c.close()

        return respone.getvalue().decode()

if __name__ == "__main__":
    req = Request("127.0.0.1:8000")
    print(req.get_json(0))