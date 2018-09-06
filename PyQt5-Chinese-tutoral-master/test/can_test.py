#coding:utf-8
from ctypes import *
import serial



VCI_USBCAN2 = 4
STATUS_OK = 1
# com = serial.Serial()
# ser = serial.Serial('COM6',115200,timeout=0.5)


class CanCfg(Structure):
    _fields_ = [("AccCode", c_ulong),
                ("AccMask", c_ulong),
                ("Reserved ", c_ulong),
                ("Filter", c_ubyte),
                ("Timing0", c_ubyte),
                ("Timing1", c_ubyte),
                ("Mode", c_ubyte)]

class Canobj(Structure):
    _fields_ =[
                ("ID",c_uint),
                ("TimeStamp",c_uint),
                ("TimeFlag",c_byte),
                ("SendType",c_byte),
                ("RemoteFlag",c_byte),
                ("ExternFlag",c_byte),
                ("DataLen",c_byte),
                ("Data",c_byte*8),
                ("Reserved",c_byte*3)]
# vci_can_obj = Canobj(0x0, 0, 0, 1, 0, 0, 8, a, b)
class Errobj(Structure):
    _fields_ =[
                ("ErrCode",c_ulong),
                ("Passive_ErrData",c_byte*3),
                ("ArLost_ErrData",c_byte)]

canDllName = 'ControlCAN.dll'
lib = windll.LoadLibrary(canDllName)
print(canDllName)
vci_initconfig = CanCfg()
vci_initconfig.AccCode = 1 << 21
vci_initconfig.AccMask = 3 << 21
vci_initconfig.Filter = 1
vci_initconfig.Timing0 = 0
vci_initconfig.Timing1 = 28
vci_initconfig.Mode = 0

VCI_OpenDevice_OK = lib.VCI_OpenDevice(4,0,1)
print('VCI_OpenDevice_OK = '+str(VCI_OpenDevice_OK))
if VCI_OpenDevice_OK != STATUS_OK:
    print('调用VCI_OpenDevice出错')

VCI_InitCAN_OK = lib.VCI_InitCAN(VCI_USBCAN2,0,1,byref(vci_initconfig))
print('VCI_InitCAN_OK = '+str(VCI_InitCAN_OK))
if VCI_InitCAN_OK != STATUS_OK:
    print('调用VCI_InitCAN出错')

VCI_StartCAN_OK = lib.VCI_StartCAN(VCI_USBCAN2,0,1)
if VCI_StartCAN_OK != STATUS_OK:
    print('调用VCI_StartCAN出错')
ubyte_array = c_ubyte * 8
# a = ubyte_array(1,2,3,4,5,6,7,1)
# a = (1,2,3,4,5,6,7,1)
# ubyte_3array = c_ubyte * 3
# b = ubyte_3array(0,0,0)
# b = (0,0,0)
# vci_can_obj = Canobj(3, 0, 0, 1, 0, 0,  8, a, b)
sd = b'\x16\x00\x03\x01\x00\x00\x00\x00'
vci_can_obj = Canobj()
# vci_can_obj.Data[0] = 0x17
# vci_can_obj.Data[1] = 0x00
# vci_can_obj.Data[2] = 0x00
# vci_can_obj.Data[3] = 0x00
# vci_can_obj.Data[4] = 0x00
# vci_can_obj.Data[5] = 0x00
# vci_can_obj.Data[6] = 0x00
# vci_can_obj.Data[7] = 0x00

bytelist = b''
bytelist += bytes([22])
bytelist += bytes([0])
bytelist += bytes([3])
bytelist += bytes([1])
bytelist += bytes([0])
bytelist += bytes([0])
bytelist += bytes([0])
bytelist += bytes([0])
print('bytelist= '+str(bytelist))
vci_can_obj.RemoteFlag = 0x00
vci_can_obj.ExternFlag = 0x00
vci_can_obj.ID = 3
vci_can_obj.DataLen = 0x08
for i in range(0, 8):
    vci_can_obj.Data[i] = bytelist[i]
    # print(vci_can_obj.Data[i])
print('vci_can_obj = ' + str(vci_can_obj.Data))
ret = lib.VCI_Transmit(VCI_USBCAN2, 0, 1, byref(vci_can_obj), 1)
print('rett= '+str(ret))
print(byref(vci_can_obj))
if ret != STATUS_OK:
    print('调用 VCI_Transmit 出错\r\n')

# 通道1接收数据
# a = ubyte_array(0, 0, 0, 0, 0, 0, 0, 0)
# a = (0, 0, 0, 0, 0, 0, 0, 0)
# vci_can_obj = Canobj(0x0, 0, 0, 1, 0, 0, 8, a)
while 1:
    ret = lib.VCI_Receive(VCI_USBCAN2, 0, 1, byref(vci_can_obj), 1, 0)
    # print('VCI_Receive_ret = ' + str(ret))
# while ret <= 0:
#     print('调用 VCI_Receive 出错\r\n')
#     ret = lib.VCI_Receive(VCI_USBCAN2, 0, 1, byref(vci_can_obj), 1, 0)
    if ret > 0:
        print(vci_can_obj.DataLen)
        print(list(vci_can_obj.Data))

# 关闭
lib.VCI_CloseDevice(VCI_USBCAN2, 0)



# opendev=lib.VCI_OpenDevice
# initcan=lib.VCI_InitCAN
# startcan=lib.VCI_StartCAN
# senddata=lib.VCI_Transmit
# closedev=lib.VCI_CloseDevice
# receivenum=lib.VCI_GetReceiveNum
# receivedata=lib.VCI_Receive
# readerrinfo=lib.VCI_ReadErrInfo
# resetcan = lib.VCI_ResetCAN
# GetSet = lib.VCI_GetReference2
#
# cancfg = CanCfg()
#
# cancfg.AccCode = 1 << 21
# cancfg.AccMask = 3 << 21
# cancfg.Filter = 1
# cancfg.Timing0 = 0
# cancfg.Timing1 = 28
# cancfg.Mode = 0
#
# cobj = Canobj()
# errobj = Errobj()
# devtype = 4
# devindex = 0
# canindex = 0
# devopen = False