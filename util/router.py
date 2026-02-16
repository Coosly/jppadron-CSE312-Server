from util.response import Response
from util.route import Route

class Router:

    def __init__(self):
        self.route_list = []
        pass

    def add_route(self, method, path, action, exact_path=False):
        self.route_list.append(Route(method, path, action, exact_path))
        pass

    def route_request(self, request, handler):
        for route in self.route_list:
            if route.method == request.method:
                if route.exact_path:
                    if request.path == route.path:
                        route.action(request, handler)
                else :
                    if request.path.startswith(route.path):
                        route.action(request, handler)
        res = Response()
        res.set_status(404, "Not Found")
        res.text("bruh")
        handler.request.sendall(res.to_data())
        pass
