import os



# def creatFolder():
my_path = os.path.abspath('main.py')
base_path = os.path.dirname(my_path)
print('mypath:'+ my_path)
print('basepath:'+ base_path)
print(os.path.exists(base_path+'/pre_dbc'))
if os.path.exists(base_path+'/pre_dbc'):
    try:
        dbc_pre1 = open(base_path+'/pre_dbc/dbc_pre1.txt','r')
        # print(dbc_pre1.read())
    except IOError:
        print('dbc_pre file error')
    finally:
        if dbc_pre1:
            dbc_pre1.close()
else:
    print('Check:[pre_dbc] folder is not exists!')
