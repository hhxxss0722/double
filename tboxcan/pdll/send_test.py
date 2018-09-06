import pdll
import sendcan


dll='ControlCAN.dll'
cdev=pdll.CanDev(dll)
cdev.SetDev([4,0,1])
# print(cdev.cancfg.AccCode)

opendev_ok = cdev.opendev(cdev.devtype,cdev.devindex,1)
print('opendev_ok= '+str(opendev_ok))

initCan_OK = cdev.InitCanDefault()
print('initCan_OK = '+str(initCan_OK))

startCan_Ok = cdev.startcan(4,0,1)
print('startCan_Ok = '+str(startCan_Ok))

scd = sendcan.SendCanData()
sd = b'' + scd.GetCanData(18,{})
print('sd = ' + str(sd))
ed = scd.GetEnd()
sendData_ok = cdev.SendData(sd)
print('sendData_ok = ' +str(sendData_ok))
