#encoding:utf8
import random

from model.user import User
from model.todo import Todo
from utils import template

import sys
reload(sys)
sys.setdefaultencoding('utf8')

session = {}

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


def index_route(request):
    """
    返回index页面的response
    """
    user = current_user(request)
    if user:
        username = user.username
    else:
        username = u'asd'
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection:Close\r\n'
    body = template('index.html', username= username)
    r = header + '\r\n' + body
    return r


def register(request):
    if request.Method == 'GET':
        header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection:Close\r\n'
        body = template('register.html')
        r = header + '\r\n' + body
        return r
    if request.Method == 'POST':
        user = User(request.form())
        if user:
            my_word = ''
            if user.register_verify():
                user.save()
                my_word = '注册成功'
            else:
                my_word = '用户名或密码格式不正确'
            header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection:Close\r\n'
            body = template('login_success.html', {'my_word':my_word})
            r = header + '\r\n' + body
            return r


def login_route(request):
    if request.Method == 'GET':
        header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection:Close\r\n'
        verify_session = request.cookies().get('username', '')
        username = session.get(verify_session, '')
        user = User.find_by(username)
        if user is not None:
            return redirect('/')
        else:
            body = template('login.html')
        r = header + '\r\n' + body
        return r
    if request.Method == 'POST':
        re_username = request.form().get('username', '')
        re_password = request.form().get('password', '')
        user = User.login_verify(re_username, re_password)
        if user:
            """如果登录成功，获取一个随机16位的字符串，和username一起放入session字典中"""
            user_session = create_session()
            session[user_session] = user.username
            return redirect('/', user_session)
        else:
            print '登录失败'
            my_word = '登录失败'
            header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection:Close\r\n'
            body = template('login_success.html',
                            my_word = my_word,)
            r = header + '\r\n' + body
            return r


def secret_route(request):
    return redirect('/')


@login_required
def todo_route(request):
    if request.Method == 'GET':
        user = current_user(request)
        todo_models = Todo.find(user_id=user.id)
        header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection:Close\r\n'
        body = template('todo.html', todo_models = todo_models)
        r = header + '\r\n' + body
        return r


@login_required
def add_todo(request):
    if request.Method == 'POST':
        form = request.form()
        user = current_user(request)
        if not user:
            return redirect('/404')
        form['user_id'] = user.id
        todo = Todo(form)
        if form.get('content', ''):
            print '我不是空的！'
            todo.save()
        return redirect('/todo')


@login_required
def edit_todo(request):
    if request.Method == 'GET':
        todo_id = request.query.get('id', '')
        if not todo_id:
            return handle_404()
        todo_id = int(todo_id)
        #根据前台get请求中的todo_id查找todo的条目
        t = Todo.find_by_id(todo_id)
        if not t:
            return handle_404()
        header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection:Close\r\n'
        body = template('todo_update.html', {
            'todo_id':t.id,
            'todo_content':t.content.encode('utf8'),
        })
        r = header + '\r\n' + body
        return r
    if request.Method == 'POST':
        todo_id = int(request.form().get('id', ''))
        todo_content = request.form().get('content', '')
        t = Todo.find_by_id(todo_id)
        t.content = todo_content
        t.save()
        return redirect('/todo')


@login_required
def delete_todo(request):
    if request.Method == 'GET':
        user = current_user(request)
        todo_id = request.query.get('id', '')
        if not todo_id:
            return handle_404()
        t = Todo.find_by_id(int(todo_id))
        if not t:
            return handle_404()
        if t.user_id != user.id:
            return handle_404()
        t.remove()
        return redirect('/todo')


@login_required
def logout_route(request):
    if request.Method == 'GET':
        session.clear()
        return redirect('/login')


#path到route的映射
route_dict = {
    '/404': handle_404,
    '/': index_route,
    '/login': login_route,
    '/logout': logout_route,
    '/reg': register,
    '/secret': secret_route,
    '/todo': todo_route,
    '/todo/add': add_todo,
    '/todo/update': edit_todo,
    '/todo/delete': delete_todo,
}
