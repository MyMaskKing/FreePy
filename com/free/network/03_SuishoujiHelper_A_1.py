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
import urllib.request
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
result_excel_path = r"C:\myfree_config\freePy\network\SuishoujiHelper\作业报告\第一步_随手记自动记账规则制定.xlsx"

#####################################################
### 00_3:Excel 样式
###
######################################################
workbook = xlsxwriter.Workbook(result_excel_path);
format_disable = workbook.add_format({
    "fg_color": "#969486","font_color": "#EEECE1"  # 字体颜色
    })
format1 = workbook.add_format({
    'font_color': 'red','bold': True,
})
format2 = workbook.add_format({'bold': True, 'font_color': '#6600FF',"fg_color": "#FFCC99",})
#####################################################
### 1，开始工作，创建【随手记自动记账规则制定】文件
######################################################
def doWork():
    ####################
    # 创建sheet
    ####################
    rule_define_sheet = workbook.add_worksheet("自定义规则")
    rule_define_sheet.set_column("A:C", 30)
    
    # 自定义规则Sheet第一行
    excel_row_data_write_format(getNextRowNumOfRuleDefineSheet(),rule_define_sheet,['【分类名/分类ID/账户名/账户ID】是从随手记网站使用您的账户登录后，对您的随手记网站信息进行收集而来。'],format1)
    excel_row_data_write_format(getNextRowNumOfRuleDefineSheet(),rule_define_sheet,['为了对您的流水数据进行分类，请您对随手记网站的内容填入模糊匹配值，多个匹配值时用英文逗号【,】分割。'],format1)
    excel_row_data_write_format(getNextRowNumOfRuleDefineSheet(),rule_define_sheet,['模糊匹配值入力规则：1.多个匹配值时英文逗号分割 2.【!】不匹配，例如：!交易关闭'],format1)
    
    # Login
    driver.get(login_url);
    driver.find_element_by_id("email").send_keys("13298317423");
    driver.find_element_by_id("pwd").send_keys("cyj19970414");
    driver.find_element_by_id("loginSubmit").click();
    mydebug.logger.debug("登录成功")
    # 点击个人记账的账本
    Wait(driver, 60).until(EC.presence_of_element_located((By.XPATH, ".//*[text()='个人记账']")))
    driver.find_element_by_xpath(".//*[text()='个人记账']").click()
    mydebug.logger.debug("已选择账本【个人记账】")
    # 记一笔的Link
    Wait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//a[@href='https://www.sui.com/tally/new.do']")))
    driver.find_element_by_xpath("//a[@href='https://www.sui.com/tally/new.do']").click()
    
    # 获取随手记网站：分类
    Wait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//li[@class='ls-li ls-li2']")))
    fenlei_all = driver.find_elements_by_xpath("//li[@class='ls-li ls-li2']")
    mydebug.logger.debug("获取随手记网站：分类")
    fenlei_tem_list=[]
    fenlei_list=[]
    for fenlei_all_str in fenlei_all :
        fenlei_str = fenlei_all_str.get_attribute("outerHTML").__str__().replace('"', "'")
        fenlei_str_format_1 = fenlei_str.split("onclick='levelSelect.choose(")[1]
        fenlei_str_format_2 = fenlei_str_format_1.split(");'><span")[0]
        fenlei_str_format_3 = fenlei_str_format_2.replace("'","")
        fenlei_str_format_4 = fenlei_str_format_3.split(",")
        fenlei_tem_list.append((fenlei_str_format_4[0].replace("1",""),fenlei_str_format_4[1],fenlei_str_format_4[2]))
    # 获取随手记网站：去重
    for tmp in fenlei_tem_list :
        if tmp not in fenlei_list :
            fenlei_list.append(tmp)
            mydebug.logger.debug(tmp)
    # 获取随手记网站：账户
    mydebug.logger.debug("获取随手记网站：账户（共同）")
    zhanghu_list=[]
    zhanghu_all = driver.find_elements_by_xpath("//li[contains(@id,'tb-outAccount-1_v_')]")
    for zhanghu_all_str in zhanghu_all :
        zhanghu_str = zhanghu_all_str.get_attribute("outerHTML").__str__().replace('"', "'")
        zhanghu_str_format_1 = zhanghu_str.split("' class='' title='")
        zhanghu_id = zhanghu_str_format_1[0].replace("<li id='tb-outAccount-1_v_","")
        zhanghu_nm = zhanghu_str_format_1[1].split("' value='")[0]
        zhanghu_list.append((zhanghu_nm,zhanghu_id))
        mydebug.logger.debug(zhanghu_id + "======================" + zhanghu_nm)
    # sitePage.close();
    # 关闭所有窗口
    driver.close();
    
    ###############################################################
    # API:https://beautifulsoup.readthedocs.io/zh_CN/latest/   ####
    ###############################################################
    #domObj = BeautifulSoup(accessed_result,'html.parser')
    #mydebug.logger.debug(domObj.prettify())
    # 随手记网站：分类_支出
    excel_row_data_write(getNextRowNumOfRuleDefineSheet(),rule_define_sheet,[])
    excel_row_data_write_format(getNextRowNumOfRuleDefineSheet(),rule_define_sheet,['（随手记网站）分类名（支出）','【禁止修改】分类ID(支出)','（请入力）模糊匹配值'],format2)
    for objData in fenlei_list:
        if objData[0] == 'payout' :
            excel_row_data_write(getNextRowNumOfRuleDefineSheet(),rule_define_sheet,[objData[1],objData[2]])
    # 随手记网站：分类_收入
    excel_row_data_write(getNextRowNumOfRuleDefineSheet(),rule_define_sheet,[])
    excel_row_data_write_format(getNextRowNumOfRuleDefineSheet(),rule_define_sheet,['（随手记网站）分类名（收入）','【（禁止修改】）分类ID（收入）','（请入力）模糊匹配值'],format2)
    for objData in fenlei_list:
        if objData[0] == 'income' :
            excel_row_data_write(getNextRowNumOfRuleDefineSheet(),rule_define_sheet,[objData[1],objData[2]])
    # 随手记网站：账户
    excel_row_data_write(getNextRowNumOfRuleDefineSheet(),rule_define_sheet,[])
    excel_row_data_write_format(getNextRowNumOfRuleDefineSheet(),rule_define_sheet,['（随手记网站）账户名','【（禁止修改】）账户ID（共通）','（请入力）模糊匹配文件名'],format2)
    for obj in zhanghu_list:
        excel_row_data_write(getNextRowNumOfRuleDefineSheet(),rule_define_sheet,[obj[0],obj[1]])
    workbook.close()
    mydebug.logger.debug("Excel做成：" + result_excel_path)


####################################################
## 99-0:共通方法：Excel的行数据写入(共同)
####################################################
def excel_row_data_write(rowNum, sheetDom, dataArray):
    indexVal = 0
    for data in dataArray:
        if indexVal == 1 :
            sheetDom.write(rowNum,indexVal,data,format_disable);
        else:
            sheetDom.write(rowNum,indexVal,data);
        indexVal = indexVal + 1

####################################################
## 99-0:共通方法：Excel的行数据写入(共同)样式
####################################################
def excel_row_data_write_format(rowNum, sheetDom, dataArray, format):
    indexVal = 0
    for data in dataArray:
        if indexVal == 1 :
            sheetDom.write(rowNum,indexVal,data,format_disable);
        else:
            sheetDom.write(rowNum,indexVal,data, format);
        indexVal = indexVal + 1

rule_define_sheet_row_index = 0
# Sheet1的Row_index生成帮助
def getNextRowNumOfRuleDefineSheet():
    global rule_define_sheet_row_index
    rule_define_sheet_row_index = rule_define_sheet_row_index + 1
    return rule_define_sheet_row_index - 1

if __name__ == '__main__':
    #URL1:开放基金排行：近2年涨幅排名（前100） and 今年    涨幅排名（前100）and 不分页 and 降序
    # 1，获取基金排行网站List
    doWork()