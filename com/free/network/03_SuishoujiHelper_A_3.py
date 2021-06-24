# coding=UTF-8
'''
##############################################
随手记规则文件做成
Created on 2020年4月2日
##############################################
@author: dapao
'''
import os
import sys
import re
from selenium import webdriver
from time import sleep
import requests
import xlrd
import xlwt
from xlutils.copy import copy
import datetime
from com.free.utils import MailUtils
# 用于解决爬取的数据格式化
import io
from future.backports.misc import count
"""
※重要：共通方法的导入
"""
from com.free.constant import CommonConstants
from com.free.utils.LogUtils import getDebugObj, getErrorObj
mydebug = getDebugObj()
myerror = getErrorObj()

"""
REDME
详细解释：
本工具读取“天天基金网”（http://fund.eastmoney.com/）的指数型基金数据，通过自定义算法计算出符合预期的基金。
自定义算法：
※※※※※※※※※※※※※※※1，
"""
"""
ULRd的描述部分
"""
#开放基金排行：近2年涨幅排名（前100） and 今年涨幅排名（前100）and 不分页 and 降序
url1 = 'https://login.sui.com/'

"""
        共通函数的描述部分
"""
file_path = r"C:\working_myself\network\download\file"
excel_path = r"C:\working_myself\network\excel"
currentTime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
fileNamePrefix = r"/site_data_page_"
fileNameSuffix = ".txt"
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding=CommonConstants.ENCODING_UTF8)
sys.setrecursionlimit(1000000)

def openBrowser():
    driver = webdriver.Firefox(executable_path =r"C:\myfree_config\freePy\browser_driver\geckodriver.exe")
    driver.get(r"https://login.sui.com/");
    driver.find_element_by_id("emailt").send_keys("13298317423");
    driver.find_element_by_id("pwd").send_keys("cyj19970414");
    driver.find_element_by_class_name("loginSubmit").click();
    
    # 记一笔的Link
    driver.get(r"https://www.sui.com/tally/new.do");
    
    # 关闭单个窗口
    # sitePage.close();
    # 关闭所有窗口
    #sitePage.close();
if __name__ == '__main__':
    openBrowser()
#     MailUtils.sendmail("GetNetData", "xinxi")
#     networObj = adjustExist(url)
#     workbook = xlrd.open_workbook(file_path + r"\Py1.xlsx");
#     copy = copy(workbook)
#     copy.save(file_path + r"\Py1.xlsx")
