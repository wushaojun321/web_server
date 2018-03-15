#encoding:utf8
import time
import os
from jinja2 import FileSystemLoader, Environment


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