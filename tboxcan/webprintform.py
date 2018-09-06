#coding:utf-8
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QCoreApplication,pyqtSignal
from pyprint.pyprint import pyprint as lprint
from readxml import CheckImei,GetMainLablePath
from form.webprint import Ui_webprintForm
from covert62.covert62 import GetTboxNumber
from tfunction import httpgetdata
import json
class WebPrintwindow(QtWidgets.QWidget):
    _signal = pyqtSignal(str)
    def __init__(self,readset):  
        super(WebPrintwindow,self).__init__()  
        self.new=Ui_webprintForm()  
        self.new.setupUi(self)
        self.readset=readset
        self.readsetxml()
        self.InitShow()
        self.path=GetMainLablePath()
        self.printlable=lprint(self.path,'')
        self.gt=GetTboxNumber()

    def InitShow(self):
        self.new.txt_sbatch.setReadOnly(True)
        self.new.txt_wbatch.setReadOnly(True)
        self.new.txt_tok.setReadOnly(True)
        self.new.txt_total.setReadOnly(True)
        self.new.txt_web.setReadOnly(True)
        self.new.txt_show.setReadOnly(True)
        self.SetEditRed(self.new.txt_web,'')
        self.new.btn_print.clicked.connect(self.print)
        self.new.btn_read.clicked.connect(self.readsetxml)
        self.new.btn_web.clicked.connect(self.GetWebData)
        self.new.btn_clear.clicked.connect(self.ClearData)
        self.new.txt_imei.textChanged.connect(self.print)

    def SetEditRed(self,s,code):
        s.setText(code)
        s.setStyleSheet("background-color:red")

    def SetEditGreen(self,s,code):
        s.setText(code)
        s.setStyleSheet("background-color:yellowgreen")

    def readsetxml(self):
        try:
            self.batch=self.readset['batch']
            self.new.txt_sbatch.setText(self.batch)
            self.new.btn_read.setStyleSheet("background-color:yellowgreen")
        except Exception as e:
            self.new.btn_read.setStyleSheet("background-color:red")
            self.new.txt_show.append("读取配置失败！")

    def GetSn(self,imei):
        simei=imei[2:11]
        lcode=imei[11:]
        icode=int(simei)
        c4=int(lcode)
        sn=self.gt.GetTboxFullCode(icode,c4)
        return sn

    def GetWebData(self):
        url="http://www.che08.com/tcm-ice/ws/0.1/inspections/query?imei=868074020985707"
        sdata=httpgetdata(url)
        jdata=sdata['data']
        if len(jdata)>0:
            self.new.txt_show.append("WEB验证正常！")
            self.new.txt_show.append(jdata.decode('utf-8','replace'))
            self.new.txt_show.append(str(sdata['state']))

    def print(self):
        imei=self.new.txt_imei.text()
        if CheckImei(imei):
            try:
                url="http://www.che08.com/tcm-ice/ws/0.1/inspections/query?imei="+imei
                sdata=httpgetdata(url)
                jdata=sdata['data']
                slist=json.loads(jdata)
                sn=self.GetSn(imei)
                self.ShowGetList(slist)
                batch=slist['batch']
                sbatch=self.new.txt_sbatch
                if batch==sbatch:
                    if slist['status']==1:
                        self.SetEditGreen(self.new.txt_web,'pass')
                        self.printlable.printsn(sn)
                    else:
                        self.SetEditRed(self.new.txt_web,'err')
                        self.new.txt_show.append(str(slist))
                else:
                    self.SetEditRed(self.new.txt_web,'设置的批次与获取的批次不一致')
                    self.new.txt_show.append(str(slist))
            except Exception as e:
                print(e)
    def ClearData(self):
        self.new.txt_show.clear()
        self.new.txt_wbatch.clear()
        self.SetEditRed(self.new.txt_web,'')
        self.new.txt_imei.clear()

    def ShowGetList(self,slist):
        tc=slist['totalCount']
        pc=slist['packageCount']
        batch=slist['batch']
        model=slist['model']
        self.new.txt_wbatch.setText(batch)
        self.new.txt_tok.setText(str(pc))
        self.new.txt_total.setText(str(tc))
        self.new.txt_show.append("型号:"+model)

    def ShowBox(self,msg):
        reply = QMessageBox.information(self, "背壳打印", msg, QMessageBox.Yes)

    def closeEvent(self, event):
        #self.printlable.closeprint()
        self._signal.emit('closewebprint')    
