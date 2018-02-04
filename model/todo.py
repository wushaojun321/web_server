#encoding:utf8
from model import Model
from model import save

class Todo(Model):
    def __init__(self, form):
        self.id = form.get('id')
        self.content = form.get('content')
        self.user_id = form.get('user_id')

    @classmethod
    def get_next_id(cls):
        """
        模仿实现主键功能，调用此函数返回todo的最大id+1
        """
        all = cls.all()
        if all:
            ids = [model.id for model in all]
            return max(ids)+1
        else:
            return 1

    @classmethod
    def find_by_id(cls, id):
        """
        根据id获取todo的model对象，如果不存在，返回False
        """
        all = cls.all()
        for model in all:
            if model.id == id:
                return model
        return False

    # def update(self):
    #     """
    #
    #     :return:
    #     """
    #     all = self.all()
    #     data = [model.__dict__ for model in all]
    #     index = 0
    #     print '('*44
    #     print self.id
    #     for i in range(len(data)):
    #         print data
    #         if self.id == data[i]['id']:
    #             index = i
    #             #break的位置 一定要注意！一个缩进错误 找了半个小时
    #             break
    #     data[i] = {
    #         'id':self.id,
    #         'content':self.content,
    #     }
    #     save(self, data)







if __name__ == '__main__':
    # form = {
    #     'id':Todo.get_next_id(),
    #     'content':'eat',
    # }
    # todo = Todo(form)
    # todo.save()
    # Todo.get_next_id()
    t = Todo.find_by_id(1)
    t.remove()
