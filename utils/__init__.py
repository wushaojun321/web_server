#encoding:utf8
import time
import os
import random
from jinja2 import FileSystemLoader, Environment

from model.user import User

session = {}

def log(log_content):
    with open('../log.txt', 'a') as f:
        f.write(time.ctime() + ':' + log_content + '\n')


#获取上级目录，即D:\project\code\web_server\
path = os.path.abspath(os.path.join(os.getcwd()))  + '\\templates'
print path
#将templates路径载入装载器
loader = FileSystemLoader(path)
#生成环境，后面直接使用这个环境对模板进行操作
env = Environment(loader=loader)

def template(name, **kwargs):
    """传入模板名称和渲染的数据，返回渲染后的HTML"""
    r = env.get_template(name)
    return r.render(**kwargs)

def current_user(request):
    """
    传入request对象，返回在线用户的model的实例，如果没有，返回None
    """
    cookies = request.cookies()
    r_session = cookies.get('username', None)
    if r_session:
        username = session.get(r_session, None)
        user = User.find_by(username)
        if user:
            return user
    return None

def login_required(func):
    """判断用户是否登录的"""
    def wrap(request):
        print '你没有登录，你还想干嘛？？？'
        user = current_user(request)
        if not user:
            return redirect('/login')
        return func(request)
    return wrap

def redirect(url, cookies=None):
    print '正在重定向~'
    if not cookies:
        header = 'HTTP/1.1 302 OK\r\nLocation: {}\r\n\r\n'.format(url)
    else:
        header = 'HTTP/1.1 302 OK\r\nLocation: {}\r\nSet-Cookie: username={}\r\n\r\n'.format(url, cookies)
    return header

def create_session():
    res = ''
    s = 'fdsgfkjlofijgfdlk214543532fdsf87dsgfui'
    for i in range(16):
        res += s[random.randint(0, len(s)-1)]
    return res

def handle_404():
    """
    返回404响应的response
    """
    print '404函数被执行啦！'
    header = 'HTTP/1.1 404 not found\r\nContent-Type: text/html\r\nConnection:Close\r\n'
    body = '<h1>404</h1>'
    r = header + '\r\n' + body
    return r
