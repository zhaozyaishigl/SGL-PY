# ！/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         :2024/4/27 8:45
# Author        : smart
# @File         :send_emali_base.py
# @Software     :PyCharm

#用于建立smtp连接
import smtplib
#邮箱需要专门的MIME格式
from email.mime.text import MIMEText
#1.编写邮箱内容
msg=MIMEText('邮箱的内容-不想上课','plain','utf-8')
#发件人
msg['From']='3095789340@qq.com'
#收件人
msg['To']='3095789340@qq.com'
#邮件的标题
msg['Subject']='星期六怎末还上课'

#连接smtp服务器并发送邮件
smtp=smtplib.SMTP_SSL('smtp.qq.com') #smtp服务器地址 使用SSl模式
smtp.login('3095789340@qq.com', 'ojnlfdmgpuandhcc') #发送方邮箱和授权码
smtp.sendmail('3095789340@qq.com', '3095789340@qq.com',msg.as_string())
smtp.quit()