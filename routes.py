#encoding:utf8
from model.user import User
from model.todo import Todo
from utils import template, handle_404, create_session, redirect, login_required, current_user, session

import sys
reload(sys)
sys.setdefaultencoding('utf8')


def index_route(request):
    """
    返回index页面的response
    """
    user = current_user(request)
    if user:
        username = user.username
    else:
        username = u'【游客】'
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
            body = template('login_success.html', my_word = my_word)
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
        body = template('todo_update.html', todo_id=t.id, todo_content=t.content.encode('utf8'),)
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
