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
from functools import singledispatch 
import requests
import xlrd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as Wait
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
from asyncio.tasks import sleep
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
    Wait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//li[@title='个人记账' and @data-bookid='553039169487']")))
    driver.find_element_by_xpath("//li[@title='个人记账' and @data-bookid='553039169487']").click()
    # 记一笔的Link
    accessed_result = getPageContentByUrl(input_data_url,"suishouji");
    mydebug.logger.debug("当前访问网址内容已经获取")
    # sitePage.close();
    # 关闭所有窗口
    driver.close();
    
    ###############################################################
    # API:https://beautifulsoup.readthedocs.io/zh_CN/latest/   ####
    ###############################################################
    domObj = BeautifulSoup(accessed_result,'html.parser')
    mydebug.logger.debug(domObj.prettify())

    # 创建sheet
    workbook = xlsxwriter.Workbook(result_excel_path);
    rule_define_sheet = workbook.add_worksheet("自定义规则")
    reference_sheet = workbook.add_worksheet("自定义时参照用")
    rule_define_sheet.set_column("A:B", 30)
    excel_row_data_write(0,reference_sheet,['下记内容是从随手记网站上下载'])
    
    # 创建一种样式, 后续可以应用于单元格等区域
    format1 = workbook.add_format({
        'font_color': 'red'
    })
    format2 = workbook.add_format({'bold': True, 'font_color': 'green'})
    
    # 自定义规则Sheet第一行
    excel_row_data_write_format(getNextRowNumOfRuleDefineSheet(),rule_define_sheet,['请对下面的内容入力模糊匹配值'],format1)
    excel_row_data_write(getNextRowNumOfRuleDefineSheet(),rule_define_sheet,[])
    excel_row_data_write_format(getNextRowNumOfRuleDefineSheet(),rule_define_sheet,['（随手记网站）分类名','（请入力）模糊匹配值'],format2)
    # 随手记网站：分类
    excel_row_data_write(getNextRowNumOfReferenceSheet(),reference_sheet,['分类名','分类ID'])
    fenleiStr = domObj.find_all("li",class_="ls-li ls-li2",id=re.compile(r"ls-li-payout-"))
    for obj in fenleiStr:
        objData = obj['onclick'].split(",")
        mydebug.logger.debug("-===============" + obj['onclick'])
        excel_row_data_write(getNextRowNumOfRuleDefineSheet(),rule_define_sheet,[objData[1].replace("'","")])
        excel_row_data_write(getNextRowNumOfReferenceSheet(),reference_sheet,[objData[1].replace("'",""),objData[2].replace(");","")])
    # 随手记网站：账户
    excel_row_data_write(getNextRowNumOfReferenceSheet(),reference_sheet,[])
    excel_row_data_write(getNextRowNumOfReferenceSheet(),reference_sheet,['账户名','账户ID'])
    excel_row_data_write(getNextRowNumOfRuleDefineSheet(),rule_define_sheet,[])
    excel_row_data_write_format(getNextRowNumOfRuleDefineSheet(),rule_define_sheet,['（随手记网站）账户名','（请入力）模糊匹配值'],format2)
    accountStr = domObj.find_all("li",id=re.compile(r"tb-outAccount-1_v_"))
    for obj in accountStr:
        mydebug.logger.debug("-===============" + obj['id']+ "=======" + obj['title'])
        excel_row_data_write(getNextRowNumOfRuleDefineSheet(),rule_define_sheet,[obj['title']])
        excel_row_data_write(getNextRowNumOfReferenceSheet(),reference_sheet,[obj['title'],obj['id'].replace("tb-outAccount-1_v_","")])
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
            ,'cookie': '__vistor=78D637F71f08wxwc2; __nick=13298317423; __utmz=121176714.1624539258.19.2.utmcsr=login.sui.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __spm_bid=03969bab0a2as6f9p251141196mfd5fe; _bookTabSwitchList=1b9fc03c54dba0b4eaa5dd344ce36b50|1|0&; SESSION_COOKIE=a8e14a3d3446b0d7b8155ae885f316e7; Hm_lvt_3db4e52bb5797afe0faaa2fde5c96ea4=1624539137,1624631464,1624636409,1624707801; __utmc=121176714; SESSION=5dca7339-2fa7-40ed-af98-63b659987e8e; __utma=121176714.689405425.1615206481.1624707803.1624710944.24; __utmt=1; Hm_lpvt_3db4e52bb5797afe0faaa2fde5c96ea4=1624712541; __utmb=121176714.5.10.1624710944'
            ,'referer': 'https://www.sui.com/tally/new.do'
            ,'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"'
            ,'sec-ch-ua-mobile': '?0'
            ,'sec-fetch-dest': 'document'
            ,'sec-fetch-mode': 'navigate'
            ,'sec-fetch-site': 'same-origin'
            ,'sec-fetch-user': '?1'
            ,'upgrade-insecure-requests': '1'
            ,'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36'
        }
        webPage = requests.get(url, headers=headers)
    else:
        webPage = requests.get(url)
        #webPage = requests.get(url, headers=headers, proxies=proxy, timeout=1)
    mydebug.logger.debug("当前访问网址：%s" %url)
    mydebug.logger.debug("访问后的状态码%d" %webPage.status_code)
    #指定网站编码
#     webPage.encoding = 'gb2312'
    jsonData = webPage.text
    return jsonData

####################################################
## 99-0:共通方法：Excel的行数据写入(共同)
####################################################
def excel_row_data_write(rowNum, sheetDom, dataArray):
    indexVal = 0
    for data in dataArray:
        sheetDom.write(rowNum,indexVal,data);
        indexVal = indexVal + 1

####################################################
## 99-0:共通方法：Excel的行数据写入(共同)样式
####################################################
def excel_row_data_write_format(rowNum, excelDom, dataArray, format):
    indexVal = 0
    for data in dataArray:
        excelDom.write(rowNum,indexVal,data, format);
        indexVal = indexVal + 1

reference_sheet_row_index = 0
# Sheet1的Row_index生成帮助
def getNextRowNumOfReferenceSheet():
    global reference_sheet_row_index
    reference_sheet_row_index = reference_sheet_row_index + 1
    return reference_sheet_row_index - 1

rule_define_sheet_row_index = 0
# Sheet2的Row_index生成帮助
def getNextRowNumOfRuleDefineSheet():
    global rule_define_sheet_row_index
    rule_define_sheet_row_index = rule_define_sheet_row_index + 1
    return rule_define_sheet_row_index - 1

if __name__ == '__main__':
    #URL1:开放基金排行：近2年涨幅排名（前100） and 今年    涨幅排名（前100）and 不分页 and 降序
    # 1，获取基金排行网站List
    doWork()