#coding:utf-8
#设置模式
def AtStart(code):
    s="AT+CG\r\n"
    return s
#退出设置模式
def ATET(code):
    s="AT+ET\r\n"
    return s
#数据帧模式
def ATAT(code):
    s="AT+AT\r\n"
    return s
#设置can模式
def AtCanMode(code):
    s="AT+CAN_MODE="+code+"\r\n"
    return s
#透传帧格式设置
def AtCanFormat(code):
    s="AT+CAN_FRAMEFORMAT="+code+"\r\n"
    return s
#can波特率
def AT_CAN_BAUD(code):
    s="AT+CAN_BAUD="+code+"\r\n"
    return s
def AT_CAN_DEFAULT(code):
    s="AT+USART_PARAM=115200,0,0,0"
    return s
#can滤波器
def AT_CAN_FILTER0(code):
    s="AT+CAN_FILTER0="+code+"\r\n"
    return s
#串口设置
def AT_USART_PARAM(code):
    s="AT+USART_PARAM="+code+"\r\n"
    return s

#获取AT指令
def GetATSendValues(argument,code):
    switcher = {
        0: AtStart,
        1: ATET,
        2: ATAT,
        3: AtCanMode,
        4: AtCanFormat,
        5: AT_CAN_BAUD,
        6: AT_CAN_FILTER0,
        7: AT_USART_PARAM,
        8: AT_CAN_DEFAULT,
        }
    func = switcher.get(argument, lambda: "nothing")
    return func(code)
#验证AT格式
def CheckAt(rstr):
    slen=len(rstr)
    isok=False
    if rstr[0]=="+" and rstr[slen-1]=="\n":
        isok=True
    return isok
#获取CAN模式
def Get_Can_Mode(code):
    sl=code.split(":")
    s=""
    if sl[1]:
        if sl[1]=="0":
            s="正常模式"
        elif sl[1]=="1":
            s="回环模式"
    return s
#透传帧格式
def Get_CAN_FRAMEFORMAT(code):
    sl=code.split(":")
    fl=[]
    if sl[1]:
        fl=sl[1].split(",")
    return fl
#can滤波器
def Get_CAN_FILTER0(code):
    sl=code.split(":")
    fl=[]
    if sl[1]:
        fl=sl[1].split(",")
    return fl
#can通讯速率
def Get_CAN_BAUD(code):
    sl=code.split(":")
    s=""
    if sl[1]:
        s=sl[1]
    return s
#串口通讯速率
def Get_USART_PARAM(code):
    sl=code.split(":")
    fl=[]
    if sl[1]:
        fl=sl[1].split(",")
    return fl
#解析can at指令
def GetATRevValues(argument,code):
    switcher ={
        0:Get_Can_Mode,
        1:Get_CAN_FRAMEFORMAT,
        2:Get_CAN_FILTER0,
        3:Get_CAN_BAUD,
        4:Get_USART_PARAM,
    }
    func = switcher.get(argument,lambda:"nothing")
    return func(code)