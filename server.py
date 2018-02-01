# encoding:utf8
"""
使用socket实现web服务器功能，用户可以直接通过浏览器访问
步骤：
    1、创建、绑定、监听socket
    2、接收请求，解析请求
        获取path、query、form
    3、根据请求构造response
    4、返回response
"""
import socket
import time
import urllib

from routes import route_dict, handle_404


class Request(object):
    def __init__(self):
        self.Method = 'GET'
        self.path = ''
        self.query = {}
        self.body = ''

    def form(self):
        post_form = {}
        for i in self.body.split('&'):
            if '=' in i:
                x, y = i.split('=', 1)
                post_form[urllib.unquote(x)] = urllib.unquote(y)
        return post_form


def parse_request(request):
    """
    对request进行解析，返回path和字典类型的headers
    """
    h = request.split('\r\n')
    body = request.split('\r\n\r\n')[1]
    method = h[0].split()[0]
    path = h[0].split()[1]
    headers = {}
    query = {}
    for line in h[1:]:
        if ': ' in line:
            k, v = line.split(': ')
            headers[k] = v
    if '?' in path:
        path, q = path.split('?', 1)
        if q:
            for i in q.split('&'):
                if '=' in i:
                    x, y = i.split('=', 1)
                    query[urllib.unquote(x)] = urllib.unquote(y)
    print method, path, headers, query, body
    return method, path, headers, query, body


def get_response(request):
    """
    通过request中的path确定要调用哪一个视图函数，返回的是视图函数执行后生成的response
    """
    if request.path not in route_dict:
        r = handle_404()
    else:
        r = route_dict[request.path](request)
    return r


def run(host, port):
    print '正在监听{}:{}'.format(host, port)
    s = socket.socket()
    s.bind((host, port))
    while True:
        s.listen(5)
        connection, addr = s.accept()
        r = ''
        while True:
            _r = connection.recv(1024)
            r += _r
            if len(_r) <= 1024:
                break

        if len(r.split('\r\n')) < 2:
            continue
        print '*'*50
        print len(r)
        print '原始请求：{}'.format(r)
        print '*' * 50
        request = Request()
        request.Method , request.path, request.header, request.query, request.body = parse_request(r)
        response = get_response(request)
        print '响应：\n' + response
        connection.sendall(response)
        # connection.close()

if __name__ == "__main__":
    host = '127.0.0.1'
    port = 8888
    run(host, port)
