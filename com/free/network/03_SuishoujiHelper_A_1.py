# coding=UTF-8
'''
03_SuishoujiHelper_A_1说明：随手记网站的规则制定
Created on 2020年4月2日

@author: dapao
'''
import os
import sys
import re
from bs4 import BeautifulSoup
import requests
import xlrd
import xlsxwriter
import json
from xlutils.copy import copy
import datetime
# 用于解决爬取的数据格式化
import io
from future.backports.misc import count
from telnetlib import theNULL
from _datetime import date
import time
from selenium import webdriver
"""
※重要：共通方法的导入
"""
from com.free.utils.MailUtils import sendmail
from com.free.constant import CommonConstants
# Pojo导入
from com.free.pojo.FundDataPojo import FundDataPojo
from com.free.utils.PropertiesUtils import PropertiesUtils
config=PropertiesUtils()
from com.free.utils.LogUtils import getDebugObj, getErrorObj, MyLogger
mydebug = getDebugObj()
myerror = getErrorObj()
"""
REDME
详细解释：
本工具读取“天天基金网”（http://fund.eastmoney.com/）的指数型基金数据，通过自定义算法计算出符合预期的基金。
自定义算法：
1，
"""
#####################################################
# 00_1系统变量
#####################################################
# 当前时间(格式YYYYMMDDHHMiSS)
currentTime_YMDHMS = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
# 当前时间(格式YYYYMMDDHHMiSS)
currentTime = datetime.datetime.now()
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,CommonConstants.ENCODING_UTF8)
sys.setrecursionlimit(1000000)

#####################################################
### 00_2:URL
###
######################################################
login_url = r"https://login.sui.com/"
input_data_url = r"https://www.sui.com/tally/new.do"
driver = webdriver.Firefox(executable_path =r"C:\myfree_config\freePy\browser_driver\geckodriver.exe")
result_excel_path = r"C:\myfree_config\freePy\network\SuishoujiHelper\作业报告\随手记自动记账规则制定.xlsx"

#####################################################
### 1，开始工作，创建【随手记自动记账规则制定】文件
######################################################
def doWork():
    # Login
    driver.get(login_url);
    driver.find_element_by_id("email").send_keys("13298317423");
    driver.find_element_by_id("pwd").send_keys("cyj19970414");
    driver.find_element_by_id("loginSubmit").click();
    
    # 记一笔的Link
    accessed_result = getPageContentByUrl(input_data_url,"suishouji");
    mydebug.logger.debug("当前访问网址内容已经获取")
    # 关闭单个窗口
    # sitePage.close();
    # 关闭所有窗口
    driver.close();
    
    ###############################################################
    # API:https://beautifulsoup.readthedocs.io/zh_CN/latest/   ####
    ###############################################################
    domObj = BeautifulSoup(accessed_result,'html.parser')
    #mydebug.logger.debug(domObj.prettify())

    # 创建sheet
    workbook = xlsxwriter.Workbook(result_excel_path);
    workbook.add_worksheet("自定义规则")
    reference_sheet = workbook.add_worksheet("自定义时参照用")
    excel_row_data_write(getNextRowNum(),reference_sheet,['下记内容是从随手记网站上下载'])
    
    # 随手记网站：分类
    excel_row_data_write(getNextRowNum(),reference_sheet,['分类名','分类ID'])
    fenleiStr = domObj.find_all("li",class_="ls-li ls-li2",id=re.compile(r"ls-li-payout-"))
    for obj in fenleiStr:
        objData = obj['onclick'].split(",")
        mydebug.logger.debug("-===============" + obj['onclick'])
        excel_row_data_write(getNextRowNum(),reference_sheet,[objData[1].replace("'",""),objData[2].replace(");","")])
    # 随手记网站：账户
    excel_row_data_write(getNextRowNum(),reference_sheet,[])
    excel_row_data_write(getNextRowNum(),reference_sheet,['账户名','账户ID'])
    accountStr = domObj.find_all("li",id=re.compile(r"tb-outAccount-1_v_"))
    for obj in accountStr:
        mydebug.logger.debug("-===============" + obj['id']+ "=======" + obj['title'])
        excel_row_data_write(getNextRowNum(),reference_sheet,[obj['title'],obj['id'].replace("tb-outAccount-1_v_","")])
    workbook.close()
    mydebug.logger.debug("Excel做成：" + result_excel_path)
# 1-1获取网站的对象
def getPageContentByUrl(url,headerFlg):
    
    # 建立代理
    proxy = {
        'http': 'http://106.75.25.3:80'
    }
    # 设置请求头 (※只有基金排行网站访问时使用)
    if headerFlg == "suishouji" : 
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
            ,'accept-encoding': 'gzip, deflate, br'
            ,'accept-language': 'zh-CN,zh;q=0.9'
            ,'cache-control': 'max-age=0'
            ,'cookie': '__vistor=78D637F71f08wxwc2; __nick=13298317423; _bookTabSwitchList=1b9fc03c54dba0b4eaa5dd344ce36b50|1|0&; SESSION_COOKIE=a8e14a3d3446b0d7b8155ae885f316e7; Hm_lvt_3db4e52bb5797afe0faaa2fde5c96ea4=1624287771,1624368747,1624459185,1624539137; __spm_bid=3cdd9189ee8es6a1p61d7d9953m8f8e4; __utma=121176714.689405425.1615206481.1624459186.1624539258.19; __utmc=121176714; __utmz=121176714.1624539258.19.2.utmcsr=login.sui.com|utmccn=(referral)|utmcmd=referral|utmcct=/; SESSION=13adc4b6-de6f-42e7-ad47-a080df3a1e45; __utmt=1; Hm_lpvt_3db4e52bb5797afe0faaa2fde5c96ea4=1624540568; __utmb=121176714.8.10.1624539258'
            ,'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"'
            ,'sec-ch-ua-mobile': '?0'
            ,'sec-fetch-dest': 'document'
            ,'sec-fetch-mode': 'navigate'
            ,'sec-fetch-site': 'none'
            ,'sec-fetch-user': '?1'
            ,'upgrade-insecure-requests': '1'
            ,'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36'
        }
        webPage = requests.get(url, headers=headers)
    else:
        webPage = requests.get(url)
#     webPage = requests.get(url, headers=headers, proxies=proxy, timeout=1)
    mydebug.logger.debug("当前访问网址：%s" %url)
    mydebug.logger.debug("访问后的状态码%d" %webPage.status_code)
    #指定网站编码
#     webPage.encoding = 'gb2312'
    jsonData = webPage.text
    return jsonData

####################################################
## 99-0:共通方法：Excel的行数据写入(共同)
####################################################
def excel_row_data_write(rowNum, excelDom, dataArray):
    indexVal = 0
    for data in dataArray:
        excelDom.write(rowNum,indexVal,data);
        indexVal = indexVal + 1

row_basic_nm = 0
# Excel生成帮助
def getNextRowNum():
    global row_basic_nm
    row_basic_nm = row_basic_nm + 1
    return row_basic_nm - 1

if __name__ == '__main__':
    #URL1:开放基金排行：近2年涨幅排名（前100） and 今年    涨幅排名（前100）and 不分页 and 降序
    # 1，获取基金排行网站List
    doWork()