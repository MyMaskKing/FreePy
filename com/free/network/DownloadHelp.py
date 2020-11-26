# coding=UTF-8
'''
######注意：首行必须定义编码
######获取网站数据主类(CSDN测试)
Created on 2020年4月2日

@author: dapao
'''
import requests
from com.free.util import LogUtils
from com.free.util import MailUtils
import sys
# 用于解决爬取的数据格式化
import io
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb2312')
# sys.setrecursionlimit(1000000)
# 
# url = 'http://thunder://QUFmdHAlM0ElMkYlMkZkeSUzQWR5JTQweGxqLjJ0dS5jYyUzQTMwMTc4JTJGJTVCJUU4JUJGJTg1JUU5JTlCJUI3JUU0JUI4JThCJUU4JUJEJUJEd3d3LjJ0dS5jYyU1RCVFNSVBNCVBNyVFNSU4NiU5MiVFOSU5OSVBOSVFNSVBRSVCNi5IRDEyODAlRTklQUIlOTglRTYlQjglODUlRTUlOUIlQkQlRTglQUYlQUQlRTQlQjglQUQlRTUlQUQlOTcucm12Ylpa'
# file_path = r"E:\AboutDeveloper\Workspace_Eclipse\freePy\com\free\download"
# # 设置请求头
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36',
# }
# 
# webPage = requests.get(url, headers=headers, stream=True)
# #指定网站编码
# webPage.encoding = 'utf-8'
# outData = webPage.content
# with open(file_path + "\pyT1.mp4","wb") as f:
#     f.write(outData)

# coding: utf-8
import urllib.request
import os

url = 'https://vdept.bdstatic.com/395a767841547939487644656a587352/446b337931687462/b9a2a5f0f0189e6c03456b1e3ac6be0192d80322b144b4f624f30daa51cb465f2a95f5f4cc05e9bc72755c9b41c75bbf.mp4'  # 下载地址

filename = url[url.rindex('/') + 1:]  # 截取文件名
print('filename = ' + filename)

downloaded = '0'


def download_listener(a, b, c):
    per = 100.0 * a * b / c
    if per > 100:
        per = 100
    new_downloaded = '%.1f' % per
    global downloaded
    if new_downloaded != downloaded:
        downloaded = new_downloaded
        print('download %s%%  %s/%s' % (downloaded, a * b, c))


path = 'D:\\download\\'  # 下载目录
if not os.path.exists(path):
    os.mkdir(path)

response = urllib.request.urlretrieve(url, path + filename, download_listener)
