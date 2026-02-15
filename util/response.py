import json


class Response:
    def __init__(self):
        self.status = '200 OK'
        self.headers_ = ''
        self.cookies_ = ''
        self.content_type_ = 'Content-Type: text/plain; charset=utf-8\r\n'
        self.body_ = b''
        pass

    def set_status(self, code, text):
        codeStr = str(code)
        self.status = codeStr + ' ' + text
        pass

    def headers(self, headers):
        for header_key in headers:
            if header_key.lower() == 'content-type':
                self.content_type_ = 'Content-Type: ' + headers[header_key] + '\r\n'
                continue
            if header_key.lower() == 'content-length':
                continue
            if header_key.lower() == 'set-cookie':
                self.cookies_ = self.cookies_ + 'Set-Cookie: ' + headers[header_key] + '\r\n'
                continue
            self.headers_ += header_key + ': ' + headers[header_key] + '\r\n'
        pass

    def cookies(self, cookies):
        for cookie in cookies:
            self.cookies_ = self.cookies_ + 'Set-Cookie: ' + cookie + '=' + cookies[cookie] + '\r\n'
        pass

    def bytes(self, data):
        self.body_ += data
        pass

    def text(self, data):
        self.body_ += data.encode()
        pass

    def json(self, data):
        self.body_ = json.dumps(data).encode()
        self.content_type_ = 'Content-Type: application/json; charset=utf-8\r\n'
        pass

    def to_data(self):
        content_length_str = 'Content-Length: ' + str(len(self.body_)) + '\r\n'
        data = b'HTTP/1.1 ' + self.status.encode() + b'\r\n' + self.content_type_.encode() + content_length_str.encode() + self.headers_.encode() + self.cookies_.encode() + b'\r\n' + self.body_
        return data


def test1():
    res = Response()
    res.text("hello")
    expected = b'HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: 5\r\n\r\nhello'
    actual = res.to_data()
    print (actual)
    assert actual == expected


if __name__ == '__main__':
    test1()
