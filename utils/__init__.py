#encoding:utf8
import time
import os
from jinja2 import FileSystemLoader, Environment


def log(log_content):
    with open('../log.txt', 'a') as f:
        f.write(time.ctime() + ':' + log_content + '\n')


#获取当前目录下的templates的绝对路径
path = '{}\\templates\\'.format(os.getcwd())
path = 'D:\\project\\code\\web_server\\templates\\'
f = open(path+'index.html', 'r')
print f.read()
log('模板路径为：{}'.format(path))
# 创建一个加载器, jinja2 会从这个目录中加载模板
loader = FileSystemLoader(path)
# 用加载器创建一个环境, 有了它才能读取模板文件
env = Environment(loader=loader)

# 调用 get_template() 方法加载模板并返回
template = env.get_template('demo.html')

# 用 render() 方法渲染模板
# 可以传递参数
ns = list(range(3))
us = [
    {
        'id': 1,
        'name': 'gua',
    },
    {
        'id': 2,
        'name': '瓜',
    },
]
log(template.render(name='gua',
                    numbers=ns,
                    users=us,
                    foo=1,
                    ))

