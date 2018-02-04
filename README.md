==利用python的socket模块实现web服务器：
    程序通过server.py运行。

==实现思路：
    1、通过socket建立TCP连接并监听
    2、将通过socket接收到的HTTP请求进行解析
    3、通过HTTP里面的请求方式、路径、header决定回复什么样的内容，通过server.py里面的get_respone()函数实现
    4、调用route函数构造response
    5、通过socket发送response





==细节实现：
在TODO中加入用户，使每个用户只能操作自己的TODO，分解如下：
    1、数据库端实现user，用来保存用户账号密码
    2、view实现用户登录功能
    3、根据request中的session判断登录的用户是谁
    4、根据用户id向前台返回他的TODO

