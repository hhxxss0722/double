#!/usr/bin/python
#coding=utf-8
# modifyDate: 20120808 ~ 20120810
# 原作者为：bones7456, http://li2z.cn/
# 修改者为：decli@qq.com
# v1.2，changeLog：
# +: 文件日期/时间/颜色显示、多线程支持、主页跳转
# -: 解决不同浏览器下上传文件名乱码问题：仅IE，其它浏览器暂时没处理。
# -: 一些路径显示的bug，主要是 cgi.escape() 转义问题
# ?: notepad++ 下直接编译的server路径问题

# 修改者为：cupedy@qq.com  20171208 ~ 20171210
# v1.3，changeLog：
# +：增加断点续传功能
# +：实测发现不同操作系统之间会出现 HTTP/1.1 200 0K 被先接收，其他部分后被接收，
#    导致不能被正确解析到，采取直接wfile.write方式
# ?：修改内容只是针对项目的实际应用，简述如下：先访问Zone服务器获取upgrade server
#     再使用得到的upgrade server获取下载文件的url，下载所需的bin文件

"""
  简介：这是一个 python 写的轻量级的文件共享服务器（基于内置的SimpleHTTPServer模块），
  支持文件上传下载，只要你安装了python（建议版本2.6~2.7，不支持3.x），
  然后去到想要共享的目录下，执行：
    python SimpleHTTPServerWithUpload.py 1234
  其中1234为你指定的端口号，如不写，默认为 8080
  然后访问 http://localhost:1234 即可，localhost 或者 1234 请酌情替换。
"""

"""Simple HTTP Server With Upload.

    This module builds on BaseHTTPServer by implementing the standard GET
    and HEAD requests in a fairly straightforward manner.

"""

__version__ = "0.1"
__all__ = ["SimpleHTTPRequestHandler"]
__author__ = "bones7456"
__home_page__ = ""

import os, sys, platform
import posixpath
import BaseHTTPServer
from SocketServer import ThreadingMixIn
import threading
import urllib, urllib2
import cgi
import shutil
import mimetypes
import re
import time

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

def get_ip_address(ifname):
      import socket
      import fcntl
      import struct
      s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      return socket.inet_ntoa(fcntl.ioctl(
                                s.fileno(),
                                0x8915, # SIOCGIFADDR
                                struct.pack('256s', ifname[:15])
                                )[20:24])

class GetWanIp:
    def getip(self):
        try:
            myip = self.visit("http://ip.taobao.com/service/getIpInfo.php?ip=myip")
        except:
            print "ip.taobao.com is Error"
            try:
                myip = self.visit("http://www.bliao.com/ip.phtml")
            except:
                print "bliao.com is Error"
                try:
                    myip = self.visit("http://www.whereismyip.com/")
                except: # 'NoneType' object has no attribute 'group'
                    print "whereismyip is Error"
                    myip = "127.0.0.1"
        return myip
    def visit(self,url):
        #req = urllib2.Request(url)
        #values = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.64 Safari/537',
        #      'Referer': 'http://ip.taobao.com/ipSearch.php',
        #      'ip': 'myip'
        #     }
        #data = urllib.urlencode(values)
        opener = urllib2.urlopen(url, None, 3)
        if url == opener.geturl():
            str = opener.read()
        return re.search('(\d+\.){3}\d+',str).group(0)

def showTips():
    print ""
    print '----------------------------------------------------------------------->> '
    try:
        port = int(sys.argv[1])
    except Exception, e:
        print '-------->> Warning: Port is not given, will use deafult port: 8080 '
        print '-------->> if you want to use other port, please execute: '
        print '-------->> python SimpleHTTPServerWithUpload.py port '
        print "-------->> port is a integer and it's range: 1024 < port < 65535 "
        port = 5001

    if not 1024 < port < 65535: port = 8080
    # serveraddr = ('', port)
    print '-------->> Now, listening at port ' + str(port) + ' ...'
    osType = platform.system()
    if osType == "Linux":
        print '-------->> You can visit the URL:   http://'+ GetWanIp().getip() + ':' +str(port)
    else:
        print '-------->> You can visit the URL:   http://127.0.0.1:' +str(port)
    print '----------------------------------------------------------------------->> '
    print ""
    return ('10.23.215.30', port)
    return ('', port)

serveraddr = showTips()

def sizeof_fmt(num):
    for x in ['bytes','KB','MB','GB']:
        if num < 1024.0:
            return "%3.1f%s" % (num, x)
        num /= 1024.0
    return "%3.1f%s" % (num, 'TB')

def modification_date(filename):
    # t = os.path.getmtime(filename)
    # return datetime.datetime.fromtimestamp(t)
    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(os.path.getmtime(filename)))

class SimpleHTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    """Simple HTTP request handler with GET/HEAD/POST commands.

        This serves files from the current directory and any of its
        subdirectories. The MIME type for files is determined by
        calling the .guess_type() method. And can reveive file uploaded
        by client.

        The GET/HEAD/POST requests are identical except that the HEAD
        request omits the actual contents of the file.

    """
    # def __init__(self, request, client_address, server):
    #     self.request = request
    #     self.client_address = client_address
    #     self.server = server
    #     self.setup()
    #     try:
    #         self.handle()
    #     finally:
    #         self.finish()

    server_version = "SimpleHTTPWithUpload/" + __version__


    def do_GET(self):
        """Serve a GET request."""
        #print "....................", threading.currentThread().getName()

        f, addr_s, addr_e, message = self.send_head()
        if f:
            if message != []:
                self.log_request(200)
                if "terminalZone" in self.path:
                    message = []
                    message.append("%s" % (f.read()))
                    self.wfile.write((('').join(message)))
                elif "versions" in self.path:
                    message.append("%s" % (f.read()))
                    self.wfile.write(('').join(message))
                elif "download" in self.path:
                    if (addr_s != -1) and (addr_e != -1):
                        f.seek(addr_s)
                        message.append("%s" % (f.read(addr_e-addr_s+1)))
                        self.wfile.write(('').join(message))
                    else:
                        message.append("%s" % (f.read()))
                        self.wfile.write(('').join(message))
                else:
                    pass
            else:
                if (addr_s != -1) and (addr_e != -1):
                    f.seek(addr_s)
                    buff = f.read(addr_e)
                    self.wfile.write(buff)
                else:
                    self.copyfile(f, self.wfile)
            f.close()

    def do_HEAD(self):
        """Serve a HEAD request."""
        f, addr_s, addr_e = self.send_head()
        if f:
            f.close()

    def do_POST(self):
        """Serve a POST request."""
        r, info = self.deal_post_data()
        print r, info, "by1: ", self.client_address
        f = StringIO()
        f.write('<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">')
        f.write("<html>\n<title>Upload Result Page</title>\n")
        f.write("<body>\n<h2>Upload Result Page</h2>\n")
        f.write("<hr>\n")
        if r:
            f.write("<strong>Success:</strong>")
        else:
            f.write("<strong>Failed:</strong>")
        f.write(info)
        f.write("<br><a href=\"%s\">back</a>" % self.headers['referer'])
        f.write("<hr><small>Powered By: bones7456, check new version at ")
        f.write("<a href=\"http://li2z.cn/?s=SimpleHTTPServerWithUpload\">")
        f.write("here</a>.</small></body>\n</html>\n")
        length = f.tell()
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", str(length))
        self.end_headers()
        if f:
            self.copyfile(f, self.wfile)
            f.close()

    def deal_post_data(self):
        boundary = self.headers.plisttext.split("=")[1]
        remainbytes = int(self.headers['content-length'])
        line = self.rfile.readline()
        remainbytes -= len(line)
        if not boundary in line:
            return (False, "Content NOT begin with boundary")
        line = self.rfile.readline()
        remainbytes -= len(line)
        fn = re.findall(r'Content-Disposition.*name="file"; filename="(.*)"', line)
        if not fn:
            return (False, "Can't find out file name...")
        path = self.translate_path(self.path)
        osType = platform.system()
        try:
            if osType == "Linux":
                fn = os.path.join(path, fn[0].decode('gbk').encode('utf-8'))
            else:
                fn = os.path.join(path, fn[0])
        except Exception, e:
            return (False, "文件名请不要用中文，或者使用IE上传中文名的文件。")
        while os.path.exists(fn):
            fn += "_"
        line = self.rfile.readline()
        remainbytes -= len(line)
        line = self.rfile.readline()
        remainbytes -= len(line)
        try:
            out = open(fn, 'wb')
        except IOError:
            return (False, "Can't create file to write, do you have permission to write?")

        preline = self.rfile.readline()
        remainbytes -= len(preline)
        while remainbytes > 0:
            line = self.rfile.readline()
            remainbytes -= len(line)
            if boundary in line:
                preline = preline[0:-1]
                if preline.endswith('\r'):
                    preline = preline[0:-1]
                out.write(preline)
                out.close()
                return (True, "File '%s' upload success!" % fn)
            else:
                out.write(preline)
                preline = line
        return (False, "Unexpect Ends of data.")

    def send_head(self):
        """Common code for GET and HEAD commands.

            This sends the response code and MIME headers.

            Return value is either a file object (which has to be copied
            to the outputfile by the caller unless the command was HEAD,
            and must be closed by the caller under all circumstances), or
            None, in which case the caller has nothing further to do.

        """
        addr_s, addr_e = -1, -1
        range_sigh = -1
        strs = str(self.headers)
        if "Range: bytes=" in strs:
            range_sigh = 1
            index1 = strs.find("Range: bytes=")
            index2 = strs[index1:].find("-")
            addr_s = int(strs[index1+13:index1+index2])
            index3 = strs[index1:].find("\r\n")
            addr_e = int(strs[index1+index2+1:index1+index3])
            print "addr_s:", addr_s, addr_e
        path = self.translate_path(self.path)
        #print "path:", path
        f = None
        if os.path.isdir(path):
            if not self.path.endswith('/'):
                # redirect browser - doing basically what apache does
                self.send_response(301)
                self.send_header("Location", self.path + "/")
                self.end_headers()
                return None, -1, -1, ""
            for index in "index.html", "index.htm":
                index = os.path.join(path, index)
                if os.path.exists(index):
                    path = index
                    break
            else:
                return self.list_directory(path), -1, -1, []
        ctype = self.guess_type(path)
        try:
            # Always read in binary mode. Opening files in text mode may cause
            # newline translations, making the actual size of the content
            # transmitted *less* than the content-length!
            f = open(path, 'rb')
        except IOError:
            self.send_error(404, "File not found")
            return None, -1, -1, []
        fs = os.fstat(f.fileno())
        #print "fs:", fs
        if "imei" in self.path:
            content = ["HTTP/1.1 200 OK\r\n"]
            content.append("Server: %s\r\n" %(self.version_string()))
            content.append("Date: %s\r\n" %(self.date_time_string()))
            content.append("Content-Type: %s\r\n" %(ctype))
            if range_sigh == 1:
                content.append("Content-Length: %d\r\n" %(addr_e - addr_s + 1))
                content.append("Content-Range: bytes %d-%d/%d\r\n" %(addr_s, addr_e, fs[6]))
            else:
                content.append("Content-Length: %s\r\n" %(str(fs[6])))
            content.append("Connection: keep-alive\r\n")
            #content.append("Last-Modified: %s\r\n" % (self.date_time_string(fs.st_mtime)))
            content.append("\r\n")
            print "content:\r\n%s\r\n"% (content)
            return f, addr_s, addr_e, content
        else:
            self.send_response(200)
            self.send_header("Content-type", ctype)
            if range_sigh == 1:
                self.send_header("Content-Length", ("%d" % (addr_e - addr_s + 1)))
                self.send_header("Content-Range", ("bytes %d-%d/%d" % (addr_s, addr_e, fs[6])))
            else:
                self.send_header("Content-Length", str(fs[6]))
            self.send_header("Connection", "keep-alive")
            self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
            self.end_headers()
            return f, addr_s, addr_e, []

    def list_directory(self, path):
        """Helper to produce a directory listing (absent index.html).

            Return value is either a file object, or None (indicating an
            error). In either case, the headers are sent, making the
            interface the same as for send_head().

        """
        try:
            list = os.listdir(path)
        except os.error:
            self.send_error(404, "No permission to list directory")
            return None
        list.sort(key=lambda a: a.lower())
        f = StringIO()
        displaypath = cgi.escape(urllib.unquote(self.path))
        f.write('<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">')
        f.write("<html>\n<title>Directory listing for %s</title>\n" % displaypath)
        f.write("<body>\n<h2>Directory listing for %s</h2>\n" % displaypath)
        f.write("<hr>\n")
        f.write("<form ENCTYPE=\"multipart/form-data\" method=\"post\">")
        f.write("<input name=\"file\" type=\"file\"/>")
        f.write("<input type=\"submit\" value=\"upload\"/>")
        f.write("              ")
        f.write("<input type=\"button\" value=\"HomePage\" onClick=\"location='/'\">")
        f.write("</form>\n")
        f.write("<hr>\n<ul>\n")
        for name in list:
            fullname = os.path.join(path, name)
            colorName = displayname = linkname = name
            # Append / for directories or @ for symbolic links
            if os.path.isdir(fullname):
                colorName = '<span style="background-color: #CEFFCE;">' + name + '/</span>'
                displayname = name
                linkname = name + "/"
            if os.path.islink(fullname):
                colorName = '<span style="background-color: #FFBFFF;">' + name + '@</span>'
                displayname = name
                # Note: a link to a directory displays with @ and links with /
            filename = os.getcwd() + '/' + displaypath + displayname
            f.write('<table><tr><td width="60%%"><a href="%s">%s</a></td><td width="20%%">%s</td><td width="20%%">%s</td></tr>\n'
                    % (urllib.quote(linkname), colorName,
                    sizeof_fmt(os.path.getsize(filename)), modification_date(filename)))
        f.write("</table>\n<hr>\n</body>\n</html>\n")
        length = f.tell()
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", str(length))
        self.end_headers()
        return f

    def translate_path(self, path):
        """Translate a /-separated PATH to the local filename syntax.

            Components that mean special things to the local file system
            (e.g. drive or directory names) are ignored. (XXX They should
            probably be diagnosed.)

        """
        if "imei" in path:
            index = path.find("imei=")
            imei = path[index+5:index+20]
            if "terminalZone" in path:
                path = imei + ".txt"
                path = os.path.join(os.getcwd(), path)
            elif "versions" in path:
                path = imei + ".py"
                path = os.path.join(os.getcwd(), path)
            elif "download" in path:
                index1 = path.find("download")
                index2 = path.find("?")
                vers = path[index1+9:index2]
                path = vers + ".bin"
                path = os.path.join(os.getcwd(), path)
            else:
                pass
        else:
            # abandon query parameters
            path = path.split('?',1)[0]
            path = path.split('#',1)[0]
            path = posixpath.normpath(urllib.unquote(path))
            words = path.split('/')
            words = filter(None, words)
            path = os.getcwd()
            for word in words:
                drive, word = os.path.splitdrive(word)
                print drive, word
                head, word = os.path.split(word)
                print head, word
                if word in (os.curdir, os.pardir): continue
                path = os.path.join(path, word)
        return path

    def copyfile(self, source, outputfile):
        """Copy all data between two file objects.

            The SOURCE argument is a file object open for reading
            (or anything with a read() method) and the DESTINATION
            argument is a file object open for writing (or
            anything with a write() method).

            The only reason for overriding this would be to change
            the block size or perhaps to replace newlines by CRLF
            -- note however that this the default server uses this
            to copy binary data as well.

        """
        shutil.copyfileobj(source, outputfile, 10)

    def guess_type(self, path):
        """Guess the type of a file.

            Argument is a PATH (a filename).

            Return value is a string of the form type/subtype,
            usable for a MIME Content-type header.

            The default implementation looks the file's extension
            up in the table self.extensions_map, using application/octet-stream
            as a default; however it would be permissible (if
            slow) to look inside the data to make a better guess.

        """

        base, ext = posixpath.splitext(path)
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        ext = ext.lower()
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        else:
            return self.extensions_map['']

    if not mimetypes.inited:
        mimetypes.init() # try to read system mime.types
    extensions_map = mimetypes.types_map.copy()
    extensions_map.update({
                            '': 'application/octet-stream', # Default
                            '.py': 'text/plain',
                            '.c': 'text/plain',
                            '.h': 'text/plain',
                            })

class ThreadingServer(ThreadingMixIn, BaseHTTPServer.HTTPServer):
    pass

def test(HandlerClass = SimpleHTTPRequestHandler,
        ServerClass = BaseHTTPServer.HTTPServer):
    BaseHTTPServer.test(HandlerClass, ServerClass)

if __name__ == '__main__':
    # test()

    #单线程
    # srvr = BaseHTTPServer.HTTPServer(serveraddr, SimpleHTTPRequestHandler)

    #多线程
    srvr = ThreadingServer(serveraddr, SimpleHTTPRequestHandler)

    srvr.serve_forever()


