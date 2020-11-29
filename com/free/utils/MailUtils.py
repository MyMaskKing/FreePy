# coding=UTF-8
'''
Created on 2020年4月3日

@author: dapao
'''
import smtplib
import traceback
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from com.free.util import LogUtils
from com.free.constant import CommonConstants
from functools import singledispatch
# 请选择发件人
fromaddr = "1647470402@qq.com"
# 请选择发邮件的邮箱类型
smtpaddr = "smtp.qq.com"
# 请选择收件人
toaddrs = ["dapao1647470402@163.com"]
# 请编辑邮件主题
subject = "【自动发信】"
# 请编辑发件人的账户密码(邮件客户端授权码)
password = "gxjjlyugpylzdfgf"
currentTime = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
msg = "没有任何内容哎"

@singledispatch
def sendmail(subject, msg):
    sendmail("","","",subject,msg)


"""
@subject:邮件主题
@msg:邮件内容
@toaddrs:收信人的邮箱地址
@fromaddr:发信人的邮箱地址
@smtpaddr:smtp服务地址，可以在邮箱看，比如163邮箱为smtp.163.com
@password:发信人的邮箱密码
"""
@sendmail.register(msg)
def sendmail(fromaddr, password, toaddrs,subject, msg):
    '''
    @subject:邮件主题
    @msg:邮件内容
    @toaddrs:收信人的邮箱地址
    @fromaddr:发信人的邮箱地址
    @smtpaddr:smtp服务地址，可以在邮箱看，比如163邮箱为smtp.163.com
    @password:发信人的邮箱密码
    '''
    try:
        # 送信元は空の場合、デフォルトのメールをセットする
        if fromaddr == "":
            fromaddr = CommonConstants.DEFAULT_EMAIL1
        # 送信元のパスワードは空の場合、デフォルトのパスワードをセットする
        if password == "":
            fromaddr = CommonConstants.DEFAULT_PASSWORD1
        # 送信先は空の場合、デフォルトの送信先のアドレスをセットする
        if toaddrs == "":
            toaddrs = CommonConstants.DEFAULT_EMAIL2
        mail_msg = MIMEMultipart()
        mail_msg['Subject'] = subject
        mail_msg['From'] = fromaddr
        mail_msg['To'] = ','.join(toaddrs)
        mesContent ="发信时间:：%s \n"\
                    "内容： %s \n"\
                    %(currentTime, msg)
        mail_msg.attach(MIMEText(mesContent, 'plain', 'utf-8'))  # f发送文本文件
        # mail_msg.attach(MIMEText(msg, 'html', 'utf-8')) #发送html格式邮件
        s = smtplib.SMTP()
        s.connect(smtpaddr)  # 连接smtp服务器
        s.login(fromaddr, password)  # 登录邮箱
        s.sendmail(fromaddr, toaddrs, mail_msg.as_string())  # 发送邮件
        s.quit()
        LogUtils.getLogger().logger.info("邮件发送成功！")
    except Exception as e:
        LogUtils.getErrorLogger().logger.error("邮件发送失败！")
        LogUtils.getErrorLogger().logger.error(e)
