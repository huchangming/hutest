import logging
import winreg
import os

def logger(log_path):
    # 定义日志配置，日志级别debug，输出详细的信息
    logging.basicConfig(level=logging.DEBUG,filename=log_path,filemode='a',format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # 获取日志指针，及添加name信息
    lg = logging.getLogger('tourscool')

    # 将手动打印的日志也输出到控制台！
    stream = logging.StreamHandler()
    lg.addHandler(stream)



    return lg


if __name__ =='__main__':
    # 桌面路径的获取方式，通过注册表获取
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    desktop_path = winreg.QueryValueEx(key, 'Desktop')[0]
    log = logger(os.path.join(desktop_path, 'tours_report','log.txt')).debug('hello word')
