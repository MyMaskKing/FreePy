# coding=UTF-8
'''
######注意：首行必须定义编码
######获取网站数据主类(CSDN测试)
Created on 2020年4月2日

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
url1 = 'http://fund.eastmoney.com/data/fundranking.html#tall;c0;r2nzf,100_jnzf,100;sjnzf;pn10000;ddesc;qsd20191229;qed20201229;qdii;zq;gg;gzbd;gzfs;bbzt;sfbb'

"""
        共通函数的描述部分
"""
file_path = r"C:\working_myself\network\download\file"
excel_path = r"C:\working_myself\network\excel"
currentTime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
fileNamePrefix = r"/site_data_page_"
fileNameSuffix = ".txt"
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding=CommonConstants.ENCODING_GB2312)
sys.setrecursionlimit(1000000)

def openBrowser():
    driver = webdriver.Firefox(executable_path =r"C:\myfree_config\freePy\browser_driver\geckodriver.exe")
    driver.get(r"http://fund.eastmoney.com/163116.html?spm=search");
    driver.find_element_by_id("search-input").click();
    driver.find_element_by_id("search-input").send_keys("163116");
    driver.find_element_by_class_name("search-submit").click();
    
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
