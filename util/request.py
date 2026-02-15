class Request:

    def __init__(self, request: bytes):
        # TODO: parse the bytes of the request and populate the following instance variables

        rest, self.body = request.split(b'\r\n\r\n', 1)
        requestLine, headers =  rest.split(b'\r\n', 1)

        self.method = requestLine.split(b' ')[0].decode('ascii')
        self.path = requestLine.split(b' ')[1].decode('utf-8')
        self.http_version = requestLine.split(b' ')[2].decode('ascii')

        headers = headers.decode('ascii').strip().split('\r\n')
        header_var = {}

        for header in headers:
            key, value = header.split(':', 1)
            header_var[key.strip()] = value.strip()

        self.headers = header_var

        cookies = header_var.get('Cookie')
        cookie_var = {}

        if cookies:
            for cookie in cookies.split(';'):
                key, value = cookie.strip().split('=', 1)
                cookie_var[key] = value

        self.cookies = cookie_var


def test1():
    request = Request(b'GET / HTTP/1.1\r\nHost: localhost:8080\r\nConnection: keep-alive\r\n\r\n')
    assert request.method == "GET"
    assert "Host" in request.headers
    assert request.headers["Host"] == "localhost:8080"  # note: The leading space in the header value must be removed
    assert request.body == b""  # There is no body for this request.
    # When parsing POST requests, the body must be in bytes, not str

    # This is the start of a simple way (ie. no external libraries) to test your code.
    # It's recommended that you complete this test and add others, including at least one
    # test using a POST request. Also, ensure that the types of all values are correct

if __name__ == '__main__':
    test1()
