from util.response import Response

def public(request, handler):
    res = Response()
    res.content_type_ = type_sniff(request)
    with open(request.path.lstrip('/'), 'rb') as file:
        public_file = file.read()
        res.bytes(public_file)
        handler.request.sendall(res.to_data())



def type_sniff(request):
    path = request.path
    file_type = path.split('.')[1]
    if file_type == 'html':
        return 'Content-Type: text/html; charset=utf-8\r\n'
    elif file_type == 'jpg':
        return 'Content-Type: image/jpeg\r\n'
    elif file_type == 'jpeg':
        return 'Content-Type: image/jpeg\r\n'
    elif file_type == 'png':
        return 'Content-Type: image/png\r\n'
    elif file_type == 'ico':
        return 'Content-Type: image/x-icon\r\n'
    elif file_type == 'gif':
        return 'Content-Type: image/gif\r\n'
    elif file_type == 'webp':
        return 'Content-Type: image/webp\r\n'
    elif file_type == 'js':
        return 'Content-Type: text/javascript; charset=utf-8\r\n'
    else:
        return 'Content-Type: text/html; charset=utf-8\r\n'