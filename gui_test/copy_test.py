import win32clipboard as wc
import win32api
import time

#获取粘贴板里的内容
def getCopyTxet():
    wc.OpenClipboard()
    copytxet = wc.GetClipboardData()
    wc.CloseClipboard()
    return str(copytxet)

if __name__ == '__main__':
    #存储上次剪切板内容
    last_data = None
    while True:
        #每秒获取一次粘贴板内容
        time.sleep(1)
        data = getCopyTxet()
        #如果粘贴板的内容和上次粘贴板的内容不相同
        if data != last_data:
            #则打印粘贴板信息
            print("粘贴板有新内容：" + data)
            last_data = data