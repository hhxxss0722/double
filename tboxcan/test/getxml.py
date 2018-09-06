#coding:utf-8
import xml.etree.ElementTree as et
import os
#获取配置文件内容，用法：初始化对应的xml文件，调用get_value(name)方法，name为xml中的tag值

class Xml_Class():
    def __init__(self, path):
        dirname = os.path.dirname(__file__)
        path = dirname + path
        self.path = path
        self.xml_to_dict()

    def xml_to_dict(self):
        root = et.parse(self.path)
        p = root.findall('.')
        xml_list = {}
        for one_per in p:
            for child in one_per.getchildren():
                xml_list[child.tag] = child.text
        self.dict = xml_list
        print(self.dict)

    def get_value(self,name):
        if name in self.dict:
             value = self.dict[name]
             print(value)
             return value
        else:
            print(str(name)+'不在配置文件中')