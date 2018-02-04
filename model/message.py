#encoding:utf8
from model import Model
import time


class Message(Model):
    def __init__(self, form):
        self.content = form.get('content', '')
        self.add_time = form.get('add_time', time.strftime('%Y-%m-%d',time.localtime(time.time())))