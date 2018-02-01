#encoding:utf8

def handle_404():
    """
    返回404响应的response
    """
    header = 'HTTP/1.1 404 not found\r\nContent-Type: text/html\r\nConnection:Close\r\n'
    body = '<h1>404</h1>'
    r = header + '\r\n' + body
    return r


def index_route(request):
    """
    返回index页面的response
    """
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection:Close\r\n'
    body = '<h1>Hello Wsj</h1>'
    r = header + '\r\n' + body
    return r


def login_route(request):
    if request.Method == 'GET':
        header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection:Close\r\n'
        body = ''
        with open('login.html', 'rb') as f:
            body += f.read()
        r = header + '\r\n' + body
        return r
    if request.Method == 'POST':
        print '进入POST了'
        header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection:Close\r\n'
        body = str(request.form())
        r = header + '\r\n' + body
        return r


#path到route的映射
route_dict = {
    '/': index_route,
    '/login':login_route,
}
