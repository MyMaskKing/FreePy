from logging import handlers
import logging
"""
※重要：共通方法的导入
"""
from com.free.constant import CommonConstants
# Pojo导入
from com.free.utils.PropertiesUtils import PropertiesUtils
from _overlapped import NULL

class MyLogger(object):
    level_relations = {
        'debug':logging.DEBUG,
        'info':logging.INFO,
        'warning':logging.WARNING,
        'error':logging.ERROR,
        'crit':logging.CRITICAL
    }  # 日志级别关系映射
    def __init__(self, filename, level='info', when='D', backCount=3, fmt='【%(levelname)s】%(asctime)s - %(filename)s:%(funcName)s[line:%(lineno)d]: %(message)s'):
        self.logger = logging.getLogger(filename)
        if not self.logger.handlers:
            format_str_console = logging.Formatter(fmt)  # 设置日志格式(控制台)
            format_str_file = logging.Formatter('【%(levelname)s】%(asctime)s - %(filename)s:%(funcName)s[line:%(lineno)d]: %(message)s')  # 设置日志格式(文件)
            self.logger.setLevel(self.level_relations.get(level))  # 设置日志级别
            sh = logging.StreamHandler()  # 往屏幕上输出
            sh.setFormatter(format_str_console)  # 设置屏幕上显示的格式
            th = handlers.TimedRotatingFileHandler(filename=filename, when=when, backupCount=backCount, encoding='utf-8')  # 往文件里写入#指定间隔时间自动生成文件的处理器
            # 实例化TimedRotatingFileHandler
            # interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
            # S 秒
            # M 分
            # H 小时、
            # D 天、
            # W 每星期（interval==0时代表星期一）
            # midnight 每天凌晨
            th.setFormatter(format_str_file)  # 设置文件里写入的格式
            self.logger.addHandler(sh)  # 把对象加到logger里
            self.logger.addHandler(th)

# 所有Log文件做成
config=PropertiesUtils()
global debugLogObj
global errLogObj

# Debug对象取得
def getDebugObj():
    debugLogObj = MyLogger(config.get(CommonConstants.DEBUG_LOG_PATH_KEY), level='debug')
    return debugLogObj
# Error重写
def getErrorObj():
    errLogObj = MyLogger(config.get(CommonConstants.ERR_LOG_PATH_KEY), level='error')
    return errLogObj
