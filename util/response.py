import json


class Response:
    def __init__(self):
        self.status = '200 OK'
        self.headers_ = ''
        self.cookies_ = ''
        self.content_type_ = 'Content-Type: text/plain; charset=utf-8\r\n'
        self.body_ = b''

    def set_status(self, code, text):
        codeStr = str(code)
        self.status = codeStr + ' ' + text
        return self

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
        return self

    def cookies(self, cookies):
        for cookie in cookies:
            self.cookies_ = self.cookies_ + 'Set-Cookie: ' + cookie + '=' + cookies[cookie] + '\r\n'
        return self

    def bytes(self, data):
        self.body_ += data
        return self

    def text(self, data):
        self.body_ += data.encode()
        return self

    def json(self, data):
        data_ = json.dumps(data)
        self.body_ = data_.encode()
        self.content_type_ = 'Content-Type: application/json\r\n'
        return self

    def to_data(self):
        content_length_str = 'Content-Length: ' + str(len(self.body_)) + '\r\n'
        if "X-Content-Type-Options: nosniff" not in self.headers_:
            self.headers_ += "X-Content-Type-Options: nosniff\r\n"
        data = b'HTTP/1.1 ' + self.status.encode() + b'\r\n' + self.content_type_.encode() + content_length_str.encode() + self.headers_.encode() + self.cookies_.encode() + b'\r\n' + self.body_
        return data


def test1():
    res = Response()
    res.text("hello")
    expected = b'HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: 5\r\n\r\nhello'
    actual = res.to_data()

if __name__ == '__main__':
    test1()
