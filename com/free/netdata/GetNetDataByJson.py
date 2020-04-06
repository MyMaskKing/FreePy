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
from xlutils.copy import copy
import datetime
from com.free.util import LogUtils
from com.free.util import MailUtils
# 用于解决爬取的数据格式化
import io
from future.backports.misc import count
# Log日志
# 数据文件路径
# LogUtils.getLogger().logger.info('第一次测试')
# 网站地址(天天基金网：开方式基金净值)
url = 'http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft=all&rs=&gs=0&sc=zzf&st=desc&sd=2019-04-05&ed=2020-04-05&qdii=&tabSubtype=,,,,,&pi=1&pn=50&dx=1&v=0.9950179280023788'
file_path = r"E:\AboutDeveloper\Workspace_Eclipse\freePy\com\free\download"
excel_path = r"C:\Users\dapao\Desktop"
currentTime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
fileNamePrefix = r"/network_data_tp2_"
fileNameSuffix = ".txt"
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb2312')
sys.setrecursionlimit(1000000)

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
    webPage = requests.get(url, headers=headers, timeout=1)
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
#         fileName = file_path + fileNamePrefix + "20200405083436" + ".html"
        # 定义文件对象
        openFile = ""
        networTree = ""
        # 如果文件存在就去读取
        if(os.path.exists(fileName)) :
            LogUtils.getLogger().logger.info("文件存在,开始读取: %s" % fileName)
            openFile = open(fileName, "r", encoding='utf-8')
            # 获取网站的所有内容
            networTree = BeautifulSoup(openFile.read(), 'lxml')
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
        # 获取a标签 并且属性为#recommend-right > div.recommend-list-box.d-flex.flex-column.aside-box > ul > li:nth-child(2) > a > div > div
#         networObj = networTree.find_all(name="a", attrs={"data-report-click" : True})
        #EXCEL的TITLE
#         execelTitle = ["基金代码","基金简称","日增长值","日增长率","申购状态","赎回状态","手续费","是否可购买"]
#         execelList = []
#         try :
#             #循环Tr
#             for ntr in networTrs :
#                 execelMap = {}
#                 #循环Td
#                 for ntd in ntr.select("td") : 
#                     #基金代码
#                     if(isExistsClass(ntd,"bzdm")) :
#                         execelMap[1] = getText(ntd.text)
#                     #基金简称
#                     if (isExistsClass(ntd,"tol")) :
#                         execelMap[2] = getText(ntd.select("a")[0].text)
#                     #日增长值
#                     if (isExistsClass(ntd,"rzzz red")) :
#                         execelMap[3] = getText(ntd.text)
#                     #日增长率
#                     if (isExistsClass(ntd,"rzzl bg red")) :
#                         execelMap[4] = getText(ntd.text)
#                     #申购状态
#                     if (isExistsClass(ntd,"sgzt")) :
#                         execelMap[5] = getText(ntd.text)
#                     #赎回状态
#                     if (isExistsClass(ntd,"shzt")) :
#                         execelMap[6] = getText(ntd.text)
#                     #手续费
#                     if (isExistsClass(ntd,"zkf")) :
#                         execelMap[7] = getText(ntd.text)
#                     #是否可购买
#                     if (isExistsClass(ntd,"bi")) :
#                         execelMap[8] = getText(ntd.text)
#                 LogUtils.getLogger().logger.info("Excel数据: %s" % execelMap)
#                 execelList.append(execelMap)
#             LogUtils.getLogger().logger.info("生成Excel数据成功,总件数: %d " % len(execelList))
#         except Exception as e :
#             LogUtils.getErrorLogger().logger.error("生成Excel数据失败 % s" % e)
        return (execelTitle,execelList)

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
        for ex in execelList : 
            if 1 in ex.keys():
                add_sheet.write(index,0,label = ex[1]);
            if 2 in ex.keys():
                add_sheet.write(index,1,label = ex[2]);
            if 3 in ex.keys():
                add_sheet.write(index,2,label = ex[3]);
            if 4 in ex.keys():
                add_sheet.write(index,3,label = ex[4]);
            if 5 in ex.keys():
                add_sheet.write(index,4,label = ex[5]);
            if 6 in ex.keys():
                add_sheet.write(index,5,label = ex[6]);
            if 7 in ex.keys():
                add_sheet.write(index,6,label = ex[7]);
            if 8 in ex.keys():
                add_sheet.write(index,7,label = ex[8]);
            index = index + 1;
        workbook.save(excel_path + r'\aaa.xls')
        LogUtils.getLogger().logger.info("Excel生成成功")
    except Exception as e :
        LogUtils.getErrorLogger().logger.error("Excel生成失败 % s" % e)

if __name__ == '__main__':
    (execelTitle,execelList) = adjustExist(url)
#     writeExcel(execelTitle,execelList)
#     MailUtils.sendmail("GetNetData", "xinxi")
#     networObj = adjustExist(url)
#     workbook = xlrd.open_workbook(file_path + r"\Py1.xlsx");
#     copy = copy(workbook)
#     copy.save(file_path + r"\Py1.xlsx")
