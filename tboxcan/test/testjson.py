#coding:utf-8
from getxml import Xml_Class
import os

# text = open('para_config.txt')
# # s = type(text.read())
# txt = text.read()
# # s = json.loads(txt)
# txt = eval(txt)
# text.close()
# # print(txt)
s = Xml_Class('\wifiset.xml')

s.get_value('11')


