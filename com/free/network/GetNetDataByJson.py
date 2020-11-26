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
from bs4 import BeautifulSoup
import requests
import xlrd
import xlwt
import json
from xlutils.copy import copy
import datetime
from com.free.util import LogUtils
from com.free.util import MailUtils
# 用于解决爬取的数据格式化
import io
from future.backports.misc import count
# 网站地址(天天基金网：基金排行 --> 开放基金排行 --> 指数基金)
url = 'http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft=zs&rs=&gs=0&sc=zzf&st=desc&sd=2019-04-11&ed=2020-04-11&qdii=|&tabSubtype=,,,,,&pi=1&pn=50&dx=1&v=0.8583246398692703'
# 网页内容文件形式(路径)
file_path = r"E:\AboutDeveloper\Workspace_Eclipse\freePy\com\free\download"
# 网页内容Excel形式(路径)
excel_path = r"C:\Users\dapao\Desktop"
# 当前时间(格式YYYYMMDDHHMiSS)
currentTime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
# 网页内容文件形式(文件名)
fileNamePrefix = r"/network_data_tp2_"
# 网页内容文件形式(文件后缀)
fileNameSuffix = ".txt"
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb2312')
sys.setrecursionlimit(1000000)
# 获取多少条数控(控制变量)
selectNetDataCount = 10
# 获取网站的对象
def getJsonData(url):
    
    # 建立代理
    proxy = {
        'http': 'http://106.75.25.3:80'
    }
    # 设置请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
    }
#     webPage = requests.get(url, headers=headers, proxies=proxy, timeout=1)
    webPage = requests.get(url, headers=headers)
    LogUtils.getLogger().logger.debug("状态码%d" %webPage.status_code)
    #指定网站编码
#     webPage.encoding = 'gb2312'
    jsonData = webPage.text
    return jsonData

# 对元素中的字符串去重空格换行
def getText(str):
    return str.replace("\n", "").strip()

# 判断Class在元素中是否存在
def isExistsClass(element,classStr):
    #获取Tag自身的class，没有的话就向子Tag检索 
    if "class" not in element.attrs and not element.find_all(class_= classStr):
        return False
    if element.find_all(class_= classStr):
        return True
    classS = element.attrs["class"]
    if(len(classS) > 1) :
        clStr = " ".join(classS)
        if(clStr == classStr) :
            return True
    elif(classS[0] == classStr) :
        return True
    return False

# 判断网页是否存在
def adjustExist(url):
        # 文件路径
        fileName = file_path + fileNamePrefix + currentTime + fileNameSuffix
#         fileName = file_path + fileNamePrefix + "20200405221230" + fileNameSuffix
        # 定义文件对象
        openFile = ""
        # 如果文件存在就去读取
        if(os.path.exists(fileName)) :
            LogUtils.getLogger().logger.info("文件存在,开始读取: %s" % fileName)
            openFile = open(fileName, "r", encoding='utf-8')
            jsonDatas = openFile.read();
        # 否则创建文件
        else :
            LogUtils.getLogger().logger.info("没有文件,开始将读取网站写入文件: %s" % fileName)
            openFile = open(fileName, "w", encoding='utf-8')
            # 获取网站的所有内容
            jsonDatas = getJsonData(url)
            openFile.write(jsonDatas);
        # 关闭文件
        openFile.close()
        # 删除文件
#         os.remove(fileName)
        LogUtils.getLogger().logger.info("文件删除成功: %s" % fileName)
        LogUtils.getLogger().logger.info("JSON数据开始读取~~~")
        LogUtils.getLogger().logger.info("JSON数据获取对象数据~~~")
#         datas = jsonDatas.replace("var rankData = {datas:","").replace("}","")
        strMark1 = ":["
        strMark2 = "],"
        datas = jsonDatas[jsonDatas.index(strMark1) + 2 : jsonDatas.index(strMark2) + 1].replace("[","").replace("]","")
        splitDatas = datas.split(r'",')
        LogUtils.getLogger().logger.info("JSON数据获取对象数据= % s" % splitDatas)
        #EXCEL的TITLE
        execelTitle = ["基金代码","基金简称","日期","日增长率","增长率(周)","增长率(1月)","增长率(3月)","增长率(6月)","增长率(1年)","增长率(2年)","增长率(3年)","增长率(今年)","增长率(成立以来)","成立日期","手续费","是否可购买"]
        return (execelTitle,splitDatas)

def writeExcel(execelTitle,execelList):
    try :
        LogUtils.getLogger().logger.info("开始生成Excel")
        # 创建sheet
        workbook = xlwt.Workbook(encoding='utf-8');
        add_sheet = workbook.add_sheet("Data")
        # 打印Title
        for i in range(len(execelTitle)):
            add_sheet.write(0,i,label = execelTitle[i]);
        # 打印内容
        index = 1;
        for i in range(len(execelList)) :
            if (selectNetDataCount == i) :
                break;
            cellList = execelList[i].split(r",")
            cellListLen = len(cellList)
            #基金代码
            if(cellListLen >= 1) :
                add_sheet.write(i+1,0,label = cellList[0]);
            #基金简称
            if(cellListLen >= 2) :
                add_sheet.write(i+1,1,label = cellList[1]);
            # 日期
            if(cellListLen >= 4) :
                add_sheet.write(i+1,2,label = cellList[3]);
            #日增长率
            if(cellListLen >= 7) :
                add_sheet.write(i+1,3,label = cellList[6]);
            #增长率(周)
            if(cellListLen >= 8) :
                add_sheet.write(i+1,4,label = cellList[7]);
            #增长率(1月)
            if(cellListLen >= 9) :
                add_sheet.write(i+1,5,label = cellList[8]);
            #增长率(3月)
            if(cellListLen >= 10) :
                add_sheet.write(i+1,6,label = cellList[9]);
            #增长率(6月)
            if(cellListLen >= 11) :
                add_sheet.write(i+1,7,label = cellList[10]);
            #增长率(1年)
            if(cellListLen >= 12) :
                add_sheet.write(i+1,8,label = cellList[11]);
            #增长率(2年)
            if(cellListLen >= 13) :
                add_sheet.write(i+1,9,label = cellList[12]);
            #增长率(3年)
            if(cellListLen >= 14) :
                add_sheet.write(i+1,10,label = cellList[13]);
            #增长率(今年)
            if(cellListLen >= 15) :
                add_sheet.write(i+1,11,label = cellList[14]);
            #增长率(成立以来)
            if(cellListLen >= 16) :
                add_sheet.write(i+1,12,label = cellList[15]);
            #成立日期
            if(cellListLen >= 17) :
                add_sheet.write(i+1,13,label = cellList[16]);
            #手续费
            if(cellListLen >= 23) :
                add_sheet.write(i+1,14,label = cellList[22]);
            #是否可购买
            if(cellListLen >= 24) :
                add_sheet.write(i+1,15,label = cellList[23]);
            LogUtils.getLogger().logger.info("JSON数据获取对象数据= % s" % cellList)
        workbook.save(excel_path + r'\aaa.xls')
        LogUtils.getLogger().logger.info("Excel生成成功")
    except Exception as e :
        LogUtils.getErrorLogger().logger.error("Excel生成失败 % s" % e)

if __name__ == '__main__':
    (execelTitle,execelList) = adjustExist(url)
    writeExcel(execelTitle,execelList)
#     MailUtils.sendmail("GetNetData", "xinxi")
#     networObj = adjustExist(url)
#     workbook = xlrd.open_workbook(file_path + r"\Py1.xlsx");
#     copy = copy(workbook)
#     copy.save(file_path + r"\Py1.xlsx")
