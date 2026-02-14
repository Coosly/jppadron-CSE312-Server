import json


class Response:
    def __init__(self):
        self.status = '200 OK'
        self.headers_ = ''
        self.body_ = b''
        pass

    def set_status(self, code, text):
        codeStr = str(code)
        self.status = codeStr + ' ' + text
        pass

    def headers(self, headers):
        for header_key in headers:
            self.headers_ = self.headers + header_key + ': ' + headers[header_key] + '\r\n'
        pass

    def cookies(self, cookies):

        pass

    def bytes(self, data):
        pass

    def text(self, data):
        pass

    def json(self, data):
        pass

    def to_data(self):
        return b''


def test1():
    res = Response()
    res.text("hello")
    expected = b'HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: 5\r\n\r\nhello'
    actual = res.to_data()


if __name__ == '__main__':
    test1()
