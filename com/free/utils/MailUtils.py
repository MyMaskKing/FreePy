# coding=UTF-8
'''
Created on 2020年4月3日

@author: dapao
'''
import smtplib
import traceback
import datetime
import mimetypes,sys,os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
"""
MIME添加附件
1.判断附件的类型guess_type返回类型和编码
2.如果是文本创建MIMEText，否则创建MIMEBase
3.创建MIMEMultipart
4.使用attach向MIMEMultipart中追加对象
"""
from email.mime.base import MIMEBase
from com.free.constant import CommonConstants
from com.free.utils.LogUtils import getDebugObj, getErrorObj
mydebug = getDebugObj()
myerror = getErrorObj()
from com.free.utils.PropertiesUtils import PropertiesUtils
config=PropertiesUtils()
currentTimeAll = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
currentTimeOther = datetime.datetime.now().strftime('%m/%d %H:%M')
msg = "没有任何内容哎"

"""
@subject:邮件主题
@msg:邮件内容
@toaddrs:收信人的邮箱地址
@fromaddr:发信人的邮箱地址
@smtpaddr:smtp服务地址，可以在邮箱看，比如163邮箱为smtp.163.com
@password:发信人的邮箱密码
"""
def sendmail(subject, msg, filePath):
    '''
    @subject:邮件主题
    @msg:邮件内容
    @filePath:发送的附件的存放的全路径(没有的时候NULL)
    @toaddrs:收信人的邮箱地址 (未实装)
    @fromaddr:发信人的邮箱地址 (未实装)
    @smtpaddr:smtp服务地址，可以在邮箱看，比如163邮箱为smtp.163.com (未实装)
    @password:发信人的邮箱密码 (未实装)
    '''
    try:
        # 1,送信元は空の場合、デフォルトのメールをセットする
        fromaddr = CommonConstants.DEFAULT_EMAIL1
        # 送信元のパスワードは空の場合、デフォルトのパスワードをセットする
        password = CommonConstants.DEFAULT_PASSWORD1
        # 送信先は空の場合、デフォルトの送信先のアドレスをセットする
        toaddrs = config.get("mail_to_adr")
        #2,Mail本文填入
        mail_msg = MIMEMultipart('related')
        mail_msg['Subject'] = "【自动发信】{0} {1}".format(subject,currentTimeOther)
        mail_msg['From'] = fromaddr
        mail_msg['To'] = toaddrs
        mesContent ="发信时间:：%s \n"\
                    "尊敬的收件者： \n"\
                    "  您好，由自动化工具给您发来信息，具体内容如下：\n ※%s"\
                    %(currentTimeAll, msg)
        mail_msg.attach(MIMEText(mesContent, 'plain', 'utf-8'))  # f发送文本文件
        # mail_msg.attach(MIMEText(msg, 'html', 'utf-8')) #发送html格式邮件
        #3，使用附件模式
        if len(filePath) > 0:
            # 读取xlsx文件作为附件，open()要带参数'rb'，使文件变成二进制格式,从而使'base64'编码产生作用，否则附件打开乱码
            att = MIMEText(open(filePath, 'rb').read(), 'base64', 'utf-8')
            att['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            #下面的filename 等号(=)后面好像不能有空格
            filepathS = os.path.split(filePath)
            fil = filepathS[0]
            fileNm = filepathS[1]
            attname ='attachment; filename ='+fileNm
            att['Content-Disposition'] = attname
            mail_msg.attach(att)
        #4，开始送信
        s = smtplib.SMTP()
        s.connect(CommonConstants.SMTPADDR1)  # 连接smtp服务器
        s.login(fromaddr, password)  # 登录邮箱
        s.sendmail(fromaddr, toaddrs.split(","), mail_msg.as_string())  # 发送邮件
        s.quit()
        mydebug.logger.debug("邮件发送成功！")
    except Exception as e:
        myerror.logger.error("邮件发送失败！")
        myerror.logger.error(e)

