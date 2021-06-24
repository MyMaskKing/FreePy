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
import csv
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import requests
import xlrd
import xlwt
from xlutils.copy import copy
import datetime
from com.free.utils import MailUtils
from com.free.utils import GetNumByImg
# 用于解决爬取的数据格式化
import io
from future.backports.misc import count
from _ast import Try
from test.support import catch_threading_exception
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


####################################################
## 00_1路径
####################################################
work_file_folder_path = r"C:\myfree_config\freePy\network\SuishoujiHelper\流水数据文件"
result_file_folder_path = r"C:/myfree_config/freePy/network/SuishoujiHelper/作业报告/"
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding=CommonConstants.ENCODING_UTF8)
sys.setrecursionlimit(1000000)

####################################################
## 1,将支付宝和微信的流水文件合并成可以被随手记自动化利用的文件
####################################################
def crt_suishoujiInputFile():
    mydebug.logger.debug("开始读取工作文件")
    # Excel作成命令开启
    excelDom = xlwt.Workbook(encoding='utf-8');
    sheel1Dom = excelDom.add_sheet("随手记登录流水数据(支付宝和微信)")
    # Excel Title写入
    excel_title = ["收入/支出/转账","分类","账户","金额","时间","备注"]
    excel_row_data_write(0,sheel1Dom,excel_title)
    default_row_index_Val = 1
    # 读取对象文件夹下所有的子文件夹及文件
    for root,dirs,files in os.walk(work_file_folder_path):
        # 读取当前目录下的所有子目录
        for dir in dirs:
            print (os.path.join(root,dir))
        # 读取当前目录下的所有文件
        for file in files:
            mydebug.logger.debug("工作文件" + os.path.join(root,file))
            default_row_index_Val = all_file_data_create(os.path.join(root,file),excelDom,sheel1Dom,default_row_index_Val)
    # 流水CSV文件内容合并后保存成Excel
    excelDom.save(result_file_folder_path + "记账数据_待确认(自动记账用).xls")

####################################################
## 1-1-1,将支付宝和微信开始读取
####################################################
def all_file_data_create(file_path,excelDom,sheel1Dom,index_Val):
    work_file_nm = ""
    ######################
    # 文件类型：1支付宝 2微信 #
    ######################
    work_file_typ = 0
    default_row_index_Val = index_Val
    defined_encode = ""
    if "alipay_record_" in file_path :
        defined_encode = "gbk"
        work_file_typ = 1
    else:
        defined_encode = "utf-8"
        work_file_typ = 2
    # 开始读取支付/微信的CSV文件
    with open(file_path,encoding=defined_encode) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        # 判断当前行是否为CSV的Title
        csv_file_index = 1
        for row_data in csv_reader:
            # 当前行为CSV的Title时不读取
            if csv_file_index == 1 :
                csv_file_index = 0
                continue
            # 流水文件的单元格总数大于10的话为流水数据
            if len(row_data) > 10 :
                mydebug.logger.debug(row_data)
                # Excel数据写入
                # 用法 add_sheet.write(行,列,label=写入内容)
                if work_file_typ == 1 :
                    excel_row_data_write(default_row_index_Val,sheel1Dom,row_data)
                else :
                    excel_row_data_write(default_row_index_Val,sheel1Dom,row_data)
                default_row_index_Val = default_row_index_Val + 1
    return default_row_index_Val
####################################################
## 99-0:共通方法：Excel的行数据写入(共同)
####################################################
def excel_row_data_write(rowNum, excelDom, dataArray):
    indexVal = 0
    for data in dataArray:
        excelDom.write(rowNum,indexVal,label = data);
        indexVal = indexVal + 1
####################################################
## 99-1:共通方法：Excel的行数据写入(支付宝)
####################################################
def excel_row_data_write1(rowNum, excelDom, dataArray):
    excelDom.write(rowNum,0,label = dataArray[0]);
    excelDom.write(rowNum,1,label = dataArray[3]);
    excelDom.write(rowNum,2,label = dataArray[4]);
    excelDom.write(rowNum,3,label = dataArray[5]);
    excelDom.write(rowNum,4,label = dataArray[10]);
    excelDom.write(rowNum,5,label = dataArray[1]);
####################################################
## 99-2:共通方法：Excel的行数据写入(微信)
####################################################
def excel_row_data_write2(rowNum, excelDom, dataArray):
    excelDom.write(rowNum,0,label = dataArray[4]);
    excelDom.write(rowNum,1,label = dataArray[3]);
    excelDom.write(rowNum,2,label = dataArray[6]);
    excelDom.write(rowNum,3,label = dataArray[0]);
    excelDom.write(rowNum,3,label = dataArray[0]);
    
"""
打开浏览器
"""
def openBrowser():
    try:
        driver = webdriver.Firefox(executable_path =r"C:\myfree_config\freePy\browser_driver\geckodriver.exe")
        driver.get(r"https://degree.qingshuxuetang.com/hkd/Student/Course/CourseShow?teachPlanId=183&periodId=17&courseId=597&cw_nodeId=kcjs_4_2&category=kcjs");
        driver
        execuetElement(driver,"findClass","vjs-play-control vjs-control vjs-button vjs-playing","411122199704140098")
        img_str = GetNumByImg.processing_image(execuetElement(driver,"findName", "chkImg",""))
        mydebug.logger.debug("URL:" + execuetElement(driver,"findName", "chkImg",""))
        classObj = driver.find_element_by_class_name("vjs-play-control vjs-control vjs-button vjs-playing");
        
        mydebug.logger.debug("验证码:" + img_str)
    except Exception as e:
        print(e);
    
    # 关闭单个窗口
    # sitePage.close();
    # 关闭所有窗口
    #sitePage.close();
    
def execuetElement(diverObj,disCd,elementNm,input_val):
    sleep(5)
    var = 1;
    count = 1
    while var == 1 :
        try :
            if disCd == "name" and input_val != "" :
                diverObj.find_element_by_name(elementNm).send_keys(input_val)
                break;
            if disCd == "name" and input_val == "" :
                diverObj.find_element_by_name(elementNm).click()
                break;
            if disCd == "findName" and input_val == "" :
                return diverObj.find_element_by_name(elementNm).get_attribute("src")
            print("当前元素["+elementNm+"]第"+ count++ +"次查找")
        except Exception as e:
            print(e)
if __name__ == '__main__':
    crt_suishoujiInputFile()
#     MailUtils.sendmail("GetNetData", "xinxi")
#     networObj = adjustExist(url)
#     workbook = xlrd.open_workbook(file_path + r"\Py1.xlsx");
#     copy = copy(workbook)
#     copy.save(file_path + r"\Py1.xlsx")
