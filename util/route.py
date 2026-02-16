class Route:

    def __init__(self, method, path, action, exact_path=False):
        self.method = method
        self.path = path
        self.action = action
        self.exact_path = exact_path
