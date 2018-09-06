#-*- coding:utf-8 -*-
import datetime,re
data = "<iobd><type>9999</type><time>2017-01-11 15:19:55</time><debug><debug_infor>9082</debug_infor><debug_string>4</debug_string></debug><voltage>12.223804</voltage></iobd>"
re_9999 = "^<iobd><type>9999</type><time>(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})</time><debug><debug_infor>(-1|\d{1,4})</debug_infor>(<debug_string>(|NULL|.{0,70})</debug_string>){0,1}</debug><voltage>(\d{1,2}.\d{6})</voltage></iobd>$"

ct_9100,ct_9101,ct_9102 = 0,0,0
pk_9999 = re.search(re_9999,data)
csq_str = pk_9999.group(2)
print csq_str