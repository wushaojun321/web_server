# encoding:utf8
"""
使用socket访问网页，获取响应
"""
import socket
import ssl


def parse_url(url):
    '''传入url，返回协议，端口，域名，访问路径
    传入：https://www.cnblogs.com/aylin/p/5572104.html
    返回：protocol='https',port=443,host='www.cnblogs.com',path='/aylin/p/5572104.html'
    '''
    protocol = 'http'
    protdict = {
        'http': 80,
        'https': 443,
    }
    if url[:8] == 'https://':
        protocol = 'https'
    url = url.split('//')[1]
    i = url.find('/')
    if i == -1:
        host = url
        path = '/'
    else:
        host = url[:i]
        path = url[i:]
    port = protdict[protocol]
    if ':' in host:
        h = host.split(':')
        host = h[0]
        port = int(h[1])
    return protocol, host, port, path


def test_parse_url():
    """
    parse_url 函数很容易出错, 所以我们写测试函数来运行看检测是否正确运行
    """
    http = 'http'
    https = 'https'
    host = 'g.cn'
    path = '/'
    test_items = [
        ('http://g.cn', (http, host, 80, path)),
        ('http://g.cn/', (http, host, 80, path)),
        ('http://g.cn:90', (http, host, 90, path)),
        ('http://g.cn:90/', (http, host, 90, path)),
        #
        ('https://g.cn', (https, host, 443, path)),
        ('https://g.cn:233/', (https, host, 233, path)),
    ]
    for t in test_items:
        url, expected = t
        u = parse_url(url)
        e = "parse_url ERROR, ({}) ({}) ({})".format(url, u, expected)
        assert u == expected, e


def create_socket(protocol):
    '''
    根据protocol的值决定返回的是普通的socket对象还是ssl加密后的socket对象
    '''
    s = socket.socket()
    if protocol == 'http':
        return s
    if protocol == 'https':
        return ssl.wrap_socket(s)


def create_request(host, path):
    request = 'GET {} HTTP/1.1\r\nHost: {}\r\nConnection: close\r\n\r\n'.format(path, host)
    return request


def parse_response(response):
    """
    :param response:
    :return: 状态码、响应头、body
    """
    header, body = response.split('\r\n\r\n', 1)
    h = header.split('\r\n')
    status_code = h[0].split()[1]
    status_code = int(status_code)
    headers = {}
    for line in h[1:]:
        k, v = line.split(': ')
        headers[k] = v
    return status_code, headers, body


def get(url):
    '''
    1、解析url
    2、创建socket
    3、定制request内容
    4、发送request
    5、接收
    6、将状态码、响应头、body解析出来，并返回
    '''
    protocol, host, port, path = parse_url(url)
    print protocol, port, host, path
    s = create_socket(protocol)
    s.connect((host, port))
    request = create_request(host, path)
    print request
    s.send(request)
    response = ''
    while True:
        r = s.recv(1024)
        response += r
        if len(r) == 0:
            break
    status_code, headers, body = parse_response(response)
    print status_code, headers, body[:100]

if __name__ == '__main__':
    url = 'http://www.cnblogs.com/aylin/p/5572104.html'
    response = get(url)
    # test_parse_url()
