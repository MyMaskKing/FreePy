# coding=UTF-8
'''
##############################################
03_SuishoujiHelper_A_3说明：上传数据至随手记网站
Created on 2020年4月2日
##############################################
@author: dapao
'''
import os
import sys
import re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as Wait
from time import sleep
import requests
import openpyxl
import datetime
from com.free.utils import MailUtils
# 用于解决爬取的数据格式化
import io
from future.backports.misc import count
from pandas._libs import index
"""
※重要：共通方法的导入
"""
from com.free.constant import CommonConstants
from com.free.utils.LogUtils import getDebugObj, getErrorObj
mydebug = getDebugObj()
myerror = getErrorObj()

########################################################
###
### 00_00:系统变量
########################################################
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding=CommonConstants.ENCODING_UTF8)
sys.setrecursionlimit(1000000)
work_file_path=r"C:\myfree_config\freePy\network\SuishoujiHelper\作业报告\随手记自动记账规则制定.xlsx"

########################################################
###
### 01_00:开始作业
########################################################
def doWork():
    
    # 登录随手记网站
    driver = webdriver.Firefox(executable_path =r"C:\myfree_config\freePy\browser_driver\geckodriver.exe")
    driver.get(r"https://login.sui.com/");
    driver.find_element_by_id("email").send_keys("13298317423");
    driver.find_element_by_id("pwd").send_keys("cyj19970414");
    driver.find_element_by_id("loginSubmit").click();
    
    # 选择个人记账的Link
    driver.implicitly_wait(30)
    aa = driver.find_element_by_xpath("//li[@title='个人记账' and @data-bookid='553039169487']").text
    print(aa)
    sleep(2)
    Wait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//li[@title='个人记账' and @data-bookid='553039169487']")))
    driver.find_element_by_xpath("//li[@title='个人记账' and @data-bookid='553039169487']").click()
    # 读取Excel数据
    excel_content = readWorkExcel(work_file_path)
    
    index = 0
    for excel_row in excel_content:
        print(excel_row)
        if index == 0 :
            index = 1
            continue
        if excel_row[0] == "支出" :
            driver.implicitly_wait(30)
            driver.get(r"https://www.sui.com/tally/new.do");
            # 为了使用JS，需要判断当前ID是否加载完成
            Wait(driver, 60).until(EC.presence_of_element_located((By.ID, "tb-category-1")))
            driver.execute_script("document.getElementById('tb-category-1').value='%s'"%excel_row[2])
            Wait(driver, 60).until(EC.presence_of_element_located((By.ID, "tb-outAccount-1")))
            driver.execute_script("document.getElementById('tb-outAccount-1').value='%s'"%excel_row[4])
            #driver.find_element_by_id("tb-category-1").send_keys(excel_row[2]);
            #driver.find_element_by_id("tb-outAccount-1").send_keys(excel_row[4])
            driver.find_element_by_id("tb-outMoney-1").send_keys(excel_row[5])
            driver.find_element_by_id("tb-datepicker").clear()
            driver.find_element_by_id("tb-datepicker").send_keys(excel_row[6])
            driver.find_element_by_id("tb-memo").send_keys(excel_row[7])
            driver.find_element_by_id("tb-save").click()
            mydebug.logger.debug("上传完成")
    
    # 关闭单个窗口
    # sitePage.close();
    # 关闭所有窗口
    #sitePage.close();
########################################################
###
### 01_01:读取Excel
########################################################
def readWorkExcel(file_path):
    excel_row_list = []
    excel_all_list = []
    #获取 工作簿对象
    workbook=openpyxl.load_workbook(file_path)
    mydebug.logger.debug("开始读取Excel" + file_path)
    #获取工作簿 workbook的所有工作表
    shenames=workbook.sheetnames
    print(shenames)  #['各省市', '测试表']
    worksheet=workbook[shenames[0]]
    print(worksheet)
    for row in worksheet.rows:
        excel_row_list = []
        for cell in row:
            excel_row_list.append(cell.value)
        excel_all_list.append(excel_row_list)
    mydebug.logger.debug("Excel内容件数：%d"%len(excel_all_list))
    return excel_all_list
    
if __name__ == '__main__':
    #readWorkExcel(work_file_path)
    doWork()
#     MailUtils.sendmail("GetNetData", "xinxi")
#     networObj = adjustExist(url)
#     workbook = xlrd.open_workbook(file_path + r"\Py1.xlsx");
#     copy = copy(workbook)
#     copy.save(file_path + r"\Py1.xlsx")
