# coding:utf-8
import smtplib
from email.mime.text import MIMEText
from email.header import Header

# 第三方 SMTP 服务
mail_host = "smtp.qq.com"  # 设置服务器
mail_user = "123438115@qq.com"  # 用户名
mail_pass = "pgwhjrzdupxxxxb"  # 口令,QQ邮箱是输入授权码，在qq邮箱设置 里用验证过的手机发送短信获得，不含空格

sender = '123438115@qq.com'
receivers = ['123438115@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

message = MIMEText('python发送邮件', 'plain', 'utf-8')
message['From'] = Header("123438115@qq.com", 'utf-8')
message['To'] = Header("123438115@qq.com", 'utf-8')

subject = '使用python发送邮件的内容'
message['Subject'] = Header(subject, 'utf-8')

smtpObj = smtplib.SMTP_SSL(mail_host, 465)
smtpObj.login(mail_user, mail_pass)
smtpObj.sendmail(sender, receivers, message.as_string())
smtpObj.quit()
print (u"邮件发送成功")
