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
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import socket
import urllib

from routes import route_dict, handle_404

class Request(object):
    def __init__(self):
        self.Method = 'GET'
        self.path = ''
        self.query = {}
        self.body = ''
        self.headers = {}

    def form(self):
        post_form = {}
        for i in self.body.split('&'):
            if '=' in i:
                x, y = i.split('=', 1)
                post_form[urllib.unquote(x)] = urllib.unquote(y)
        return post_form

    def cookies(self):
        res = {}
        str_cookies = self.headers.get('Cookie', '')
        if str_cookies:
            list_cookies = str_cookies.split('; ')
            for i in list_cookies:
                k, v = i.split('=')
                res[k] = v
        return res

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
                    #这里需要对query里面的数据进行解码，如%20->&
                    query[urllib.unquote(x)] = urllib.unquote(y)
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
        """无线循环接收HTTP请求"""
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
        print '原始请求：{}'.format(r)
        print '*' * 50
        #获取request实例，并将请求内容解析后传给request实例
        request = Request()
        request.Method , request.path, request.headers, request.query, request.body = parse_request(r)
        response = get_response(request)
        print '响应：\n' + response
        connection.sendall(response)
        # connection.close()

if __name__ == "__main__":
    host = '127.0.0.1'
    port = 8888
    run(host, port)
