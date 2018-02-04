#encoding:utf8
from model import Model


class User(Model):
    def __init__(self, form):
        self.id = form.get('id')
        self.username = form.get('username', '')
        self.password = form.get('password', '')

    def register_verify(self):
        if len(self.username) < 4 and len(self.password) < 4:
            return False
        return True

    @classmethod
    def login_verify(cls, username, password):
        """
        用户登录验证，如果正确，返回user实例，如果失败返回False
        """
        user = cls.find_by(username)
        if user:
            if password == user.password:
                return user
        return False


    @classmethod
    def find_by(cls, username):
        """
        传入username，判断用户是否存在，如果存在，返回这个user实例,如果不存在，返回None
        """
        users = cls.all()
        for user in users:
            if user.username == username:
                return user
        return None


if __name__ == '__main__':
    print User.find_by('wsj').password

