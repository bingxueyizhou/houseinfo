import os
import configparser

"""
read(filename) #读取配置文件，直接读取ini文件内容

sections() #获取ini文件内所有的section，以列表形式返回['logging', 'mysql']

options(sections) #获取指定sections下所有options ，以列表形式返回['host', 'port', 'user', 'password']

items(sections) #获取指定section下所有的键值对，[('host', '127.0.0.1'), ('port', '3306'), ('user', 'root'), ('password', '123456')]

get(section, option) #获取section中option的值，返回为string类型
>>>>>获取指定的section下的option <class 'str'> 127.0.0.1

getint(section,option) 返回int类型
getfloat(section, option)  返回float类型
getboolean(section,option) 返回boolen类型
"""


def init_v2conf(path=None):
    conf_path = "./config/app.conf"
    if path is not None:
        conf_path = path

    v2conf = configparser.ConfigParser()
    conf_path_dir = os.path.dirname(conf_path)
    if not os.path.exists(conf_path_dir):
        os.makedirs(conf_path_dir)
        fid = open(conf_path, 'w')
        fid.close()

    v2conf.read(conf_path)
    return v2conf
