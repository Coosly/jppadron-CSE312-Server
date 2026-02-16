from util.response import Response

def page(request, handler):
    with open('public/layout/layout.html', 'rb') as layout_file:
        layout_html = layout_file.read()
        if request.path == '/':
            with open('public/index.html', 'rb') as index_file:
                index_html = index_file.read()
                home_page = layout_html.replace(b'{{content}}', index_html)
                res = Response()
                res.bytes(home_page)
                res.content_type_ = 'Content-Type: text/html; charset=utf-8\r\n'
                handler.request.sendall(res.to_data())
                return
        if request.path == '/chat':
            with open('public/chat.html', 'rb') as chat_file:
                chat_html = chat_file.read()
                chat_page = layout_html.replace(b'{{content}}', chat_html)
                res = Response()
                res.bytes(chat_page)
                res.content_type_ = 'Content-Type: text/html; charset=utf-8\r\n'
                handler.request.sendall(res.to_data())
                return