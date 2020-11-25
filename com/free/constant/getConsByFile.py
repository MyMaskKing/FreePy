# coding=UTF-8
'''
Created on 2020年4月11日

@author: dapao
'''
import os
class ConsFile :
    # 默认配置文件为C盘
    defaultFileP_N = r"C:\Freepy\Freepy配置文件.txt"
    
    ###############常量##########################
    url_json = "";
    file_path = r"E:\AboutDeveloper\Workspace_Eclipse\freePy\com\free\download"
    excel_path = r"C:\Users\dapao\Desktop"
    fileNamePrefix = r"/network_tp1_data_"
    ###############常量##########################
    # 如果文件存在就去读取
    if(os.path.exists(defaultFileP_N)) :
        open = open(defaultFileP_N, "r")