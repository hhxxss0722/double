#! -*- coding:utf-8 -*-
__author__ = 'yubenliu'
#!/usr/bin/python
from  BaseHTTPServer import   BaseHTTPRequestHandler,HTTPServer
class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            f=open(self.path[1:],'r') # 获取客户端输入的页面文件名称
            self.send_response(200)#如果正确返回200
            self.send_header('Content-type','text/html') #定义下处理的文件的类型
            self.end_headers()#结束处理
            self.wfile.write(f.read())#通过wfile将下载的页面传给客户
            f.close() #关闭
        except IOError:
            self.send_error(404, 'file not found: %s'%self.path)
def main():
    try:
       server=HTTPServer(('127.0.0.1',8080),MyHandler) #启动服务
       print'welcome to  the  server'
       print 'quit  jieshu'
       server.serve_forever()# 一直运行
    except KeyboardInterrupt:
        print 'shutdong  doen server'
        server.socket.close()
if  __name__=='__main__':
     main()