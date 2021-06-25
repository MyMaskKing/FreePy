# coding=UTF-8
'''
03_SuishoujiHelper_A_2说明：随手记自动化工具所使用的流水数据文件做成
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
import xlsxwriter
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

####################################################
## 00_1路径及系统变量
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
    excelDom = xlsxwriter.Workbook(result_file_folder_path + "记账数据_待确认(自动记账用).xlsx");
    sheel1Dom = excelDom.add_worksheet("随手记登录流水数据(支付宝和微信)")
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
    excelDom.close()

####################################################
## 1-1-1,支付宝和微信开始读取
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
        excelDom.write(rowNum,indexVal,data);
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
    

if __name__ == '__main__':
    crt_suishoujiInputFile()
#     MailUtils.sendmail("GetNetData", "xinxi")
#     networObj = adjustExist(url)
#     workbook = xlrd.open_workbook(file_path + r"\Py1.xlsx");
#     copy = copy(workbook)
#     copy.save(file_path + r"\Py1.xlsx")
