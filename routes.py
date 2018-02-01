#encoding:utf8
from model import User

def template(name):
    with open('templates/'+name) as f:
        return f.read()


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


def register(request):
    if request.Method == 'GET':
        header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection:Close\r\n'
        body = template('register.html')
        r = header + '\r\n' + body
        return r
    if request.Method == 'POST':
        print 'request_form:{}'.format(request.form())
        user = User(request.form())
        if user:
            my_word = ''
            if user.register_verify():
                user.save()
                my_word = '注册成功'
            else:
                my_word = '用户名或密码格式不正确'
            header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection:Close\r\n'
            body = template('login_success.html')
            body = body.format(my_word=my_word)
            r = header + '\r\n' + body
            return r


def login_route(request):
    if request.Method == 'GET':
        header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection:Close\r\n'
        body = template('login.html')
        r = header + '\r\n' + body
        return r
    if request.Method == 'POST':
        user = User(request.form())
        if user.login_verify():
            my_word = '登录成功'
        else:
            my_word = '登录失败'
        header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection:Close\r\n'
        body = template('login_success.html')
        body = body.format(my_word=my_word)
        r = header + '\r\n' + body
        return r


#path到route的映射
route_dict = {
    '/': index_route,
    '/login':login_route,
    '/reg':register,
}
