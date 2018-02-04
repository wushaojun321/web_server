# encoding:utf8

import json


def save(c, data):
    with open('db/{}.txt'.format(c.__class__.__name__), 'w', ) as f:
        print '正在保存~'
        f.write(json.dumps(data))
        print '保存成功~'


class Model(object):
    """
    ORM的基类
    """

    @classmethod
    def get_path(cls):
        """
        获取数据文件路径，文件名为类名
        :return:
        """
        path = 'db/{}.txt'.format(cls.__name__)
        return path

    @classmethod
    def all(cls):
        """
        获取model的全部实例，以列表形式返回
        """
        path = cls.get_path()
        with open(path, 'r') as f:
            f = f.read() or '[]'
            models = json.loads(f)
        res = [cls(model) for model in models]
        return res

    def save(self):
        """
        判断此实例是否与已经存在的实例内容相同，如果相同则不保存
        判断实例是否有id：
            如果没有则代表此条数据为新增数据，需要获取next_id，然后保存
            如果有则代表为修改数据
        """
        models = self.all()
        data = [model.__dict__ for model in models]
        if self.__dict__ in data:
            print '此条目已经存在！'
            return
        if self.__dict__.get('id') is not None:
            """修改已经存在的条目，id不变"""
            index = -1
            for i in range(len(data)):
                if data[i]['id'] == self.id:
                    index = i
                    break
            if index != -1:
                data[index] = self.__dict__
            else:
                print '您提供的id有误，如果要添加数据，请将self.id设为None'
                return
            save(self, data)
            print '保存成功！！！！！！！'
            return
        else:
            """获取id,添加一条数据"""
            # 这里根据id的最大数加1为新id
            if len(data) == 0:
                max_id = 0
            else:
                max_id = max([item['id'] for item in data])
            self.id = max_id + 1
            data.append(self.__dict__)
            save(self, data)
            return

    def remove(self):
        models = self.all()
        data = [model.__dict__ for model in models]
        print data[data.index(self.__dict__)]
        del data[data.index(self.__dict__)]
        save(self, data)
        print '删除成功!!!!!!!'
        return

    @classmethod
    def find(cls, **kwargs):
        """
        用法如下，kwargs 是只有一个元素的 dict
        u = User.find(user_id='1')
        返回一个包含此model实例的列表，如果没有也返回空列表
        """
        k, v = '', ''
        for key, value in kwargs.items():
            k, v = key, value
        all = cls.all()
        res = []
        for m in all:
            # getattr(m, k) 等价于 m.__dict__[k]
            if v == m.__dict__[k]:
                res.append(m)
        return res



if __name__ == '__main__':
    # print User.all()
    # form = {
    #     'username':'wll',
    #     'password':'111',
    # }
    # user = User(form)
    # user.save()
    # from message import Message
    #
    # form1 = {
    #     'content': 'hello2222',
    #     'add_time': '2018.1.1',
    # }
    # mes = Message(form1)
    # mes.save()
    # print mes.all()[0].content
    pass