# encoding:utf8

import json
import time


class Model(object):
    """
    功能：
        1、将数据写入json文件
        2、读取json文件中的数据
    """

    @classmethod
    def get_path(cls):
        """
        获取数据文件路径，文件名为类名
        :return:
        """
        path = '{}.txt'.format(cls.__name__)
        return path

    @classmethod
    def all(cls):
        path = cls.get_path()
        with open(path, 'r') as f:
            f = f.read() or '[]'
            models = json.loads(f)
        return models

    def save(self):
        model = self.all()
        if self.__dict__ not in model:
            model.append(self.__dict__)
            with open('{}.txt'.format(self.__class__.__name__), 'w',) as f:
                print '正在保存~'
                f.write(json.dumps(model))
        else:
            print '此条目已经存在！'


class User(Model):
    def __init__(self, form):
        self.username = form.get('username', '')
        self.password = form.get('password', '')

    def register_verify(self):
        if len(self.username) < 4 and len(self.password) < 4:
            return False
        return True

    def login_verify(self):
        if self.username == 'wsj' and self.password == '123':
            return True
        return False


class Message(Model):
    def __init__(self, form):
        self.content = form.get('content', '')
        self.add_time = form.get('add_time', time.strftime('%Y-%m-%d',time.localtime(time.time())))

if __name__ == '__main__':
    # print User.all()
    # form = {
    #     'username':'wll',
    #     'password':'111',
    # }
    # user = User(form)
    # user.save()
    form1 = {
        'content':'hello',
        'add_time':'2018.1.1',
    }
    mes = Message(form1)
    mes.save()
    print mes.all()