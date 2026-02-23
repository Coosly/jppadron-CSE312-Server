import socketserver

from util import chat
from util.public import public
from util.page import page
from util.request import Request
from util.router import Router
from util.hello_path import hello_path


class MyTCPHandler(socketserver.BaseRequestHandler):

    def __init__(self, request, client_address, server):
        self.router = Router()
        self.router.add_route("GET", "/public", public, False)
        self.router.add_route("GET", "/hello", hello_path, True)
        self.router.add_route("GET", "/", page, True)
        self.router.add_route("GET", "/chat", page, True)
        self.router.add_route("POST", "/api/chats", chat.create_chat, False)
        self.router.add_route("GET", "/api/chats", chat.get_chat, False)
        self.router.add_route("PATCH", "/api/chats", chat.update_chat, False)
        self.router.add_route("DELETE", "/api/chats", chat.delete_chat, False)
        self.router.add_route("PATCH", "/api/reaction", chat.add_reaction, False)
        self.router.add_route("DELETE", "/api/reaction", chat.delete_reaction, False)
        self.router.add_route("PATCH", "/api/nickname", chat.set_nickname, False)
        # TODO: Add your routes here
        super().__init__(request, client_address, server)

    def handle(self):
        received_data = self.request.recv(2048)
        print(self.client_address)
        print("--- received data ---")
        print(received_data)
        print("--- end of data ---\n\n")
        request = Request(received_data)

        self.router.route_request(request, self)


def main():
    host = "0.0.0.0"
    port = 8080
    socketserver.ThreadingTCPServer.allow_reuse_address = True

    server = socketserver.ThreadingTCPServer((host, port), MyTCPHandler)

    print("Listening on port " + str(port))
    server.serve_forever()


if __name__ == "__main__":
    main()
