# encoding:utf8
"""
使用socket实现web服务器功能，用户可以直接通过浏览器访问
步骤：
    1、创建、绑定、监听socket
    2、
"""
import socket
import time


# s = socket.socket()
# host = '127.0.0.1'
# port = 8888
# s.bind((host, port))
# s.listen(5)
# s1, addr = s.accept()
# request = s1.recv(1024)
# print request
# header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
# body = '<h1>Hello Gua</h1>'
# r = header + '\r\n' + body
# s1.sendall(r)


def handle_404():
    """
    返回404响应的response
    """
    header = 'HTTP/1.1 404 not found\r\nContent-Type: text/html\r\nConnection:Close\r\n'
    body = '<h1>404</h1>'
    r = header + '\r\n' + body
    return r


def index_route():
    """
    返回index页面的response
    """
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection:Close\r\n'
    body = '<h1>Hello Wsj</h1>'
    r = header + '\r\n' + body
    return r

#path到route的映射
route_dict = {
    '/': index_route,
}


def parse_request(request):
    """
    对request进行解析，返回path和字典类型的headers
    """
    h = request.split('\r\n')
    path = h[0].split()[1]
    headers = {}
    for line in h[1:]:
        if line == '':
            continue
        k, v = line.split(': ')
        headers[k] = v
    return path, headers


def get_response(request):
    """
    通过request中的path确定要调用哪一个视图函数，返回的是视图函数执行后生成的response
    """
    path, headers = parse_request(request)
    if path not in route_dict:
        r = handle_404()
    else:
        r = route_dict[path]()
    return r


def run(host, port):
    s = socket.socket()
    s.bind((host, port))
    s.listen(5)
    print '正在监听{}:{}'.format(host,port)
    connection, addr = s.accept()
    request = ''
    while True:
        r = connection.recv(1024)
        request += r
        if len(r) <= 1024:
            break
    print '请求头：\n' + request
    response = get_response(request)
    print '响应：\n' + response
    connection.sendall(response)


if __name__ == "__main__":
    host = '127.0.0.1'
    port = 8888
    run(host, port)
