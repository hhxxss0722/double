#-*- coding:utf-8 -*-
import paramiko
import time
import datetime
import var_ssh

def main():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(var_ssh.Host,var_ssh.port,var_ssh.user,var_ssh.passwd)
    print "start.",datetime.datetime.now()
    try:
        if 1:
            list_cmm = ["python /home/xiaoliujun/dmn_script/main.py test ym 1",\
                        "python /home/xiaoliujun/dmn_script/main.py flsh ym 1",\
                       ]
        else:
            list_cmm = ["python /home/xiaoliujun/dmn_script/main.py zhqt ym 1",\
                        "python /home/xiaoliujun/dmn_script/main.py lecheng ym 1",\
                        "python /home/xiaoliujun/dmn_script/main.py abnormal ym 1",\
                        "python /home/xiaoliujun/dmn_script/main.py zhqt ym 1",\
                        "python /home/xiaoliujun/dmn_script/main.py volt ym 1",\
                        "python /home/xiaoliujun/dmn_script/main.py rpmn ym 1",\
                        "python /home/xiaoliujun/dmn_script/main.py rpmy ym 1",\
                        "python /home/xiaoliujun/dmn_script/main.py flsh ym 1",\
                        "python /home/xiaoliujun/dmn_script/main.py test ym 1",\
                        "python /home/xiaoliujun/dmn_script/main.py baoxian ym 1",\

                    ]
        
        for cmm in list_cmm:
            print cmm,datetime.datetime.now()
            (stdin, stdout, stderr) = ssh.exec_command(cmm)
            st = stdout.readlines()
            legh = len(st)
            print st,legh
            if st[legh-1].strip() != "success!":
                print "break,",st[legh-1].strip()
                break
            else:
                print "success.."

    except Exception,ex:
        print Exception,ex
    finally:
        ssh.close()
    print "ssh.close."

if __name__ == '__main__':
    main()
    #raw_input("please...")