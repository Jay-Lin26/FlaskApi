from email.mime.text import MIMEText
from connection import select
from random import randint
import hashlib
import smtplib
import time, datetime

""" 密码加密"""


def encryption(password):
    # 生成md5对象
    md5 = hashlib.md5(b'zhou')
    # 对数据加密
    md5.update(password.encode('utf8'))
    # 获取密文
    pwd = md5.hexdigest()
    return pwd


""" 邮箱验证码 """


def Email_code():
    code = ''
    string_code = 'abcdefghijklmnopqrstuvwxyz1234567890'
    for k in range(6):
        code = string_code[randint(0, 35)] + code
    return code


""" 发送邮件 """


def send_email(user_email):
    # 第三方 smtp 服务
    mail_host = 'smtp.163.com'
    mail_user = 'z64666760@163.com'
    password = 'YZYPMEHFIAXZPQLJ'       # 需要使用授权码

    sender = 'z64666760@163.com'
    # 需要发送的邮件内容
    """ 随机验证码 """
    code = Email_code()
    content = MIMEText('您的验证码是：%s' % code)
    content['Subject'] = '登录验证码'     # 邮件主题
    content['From'] = sender        # 发件人
    content['To'] = user_email        # 收件人
    # 连接邮箱服务器；smtp端口是25
    try:
        smtp = smtplib.SMTP()
        smtp.connect(mail_host, port=25)
        smtp.login(mail_user, password)    # 登录邮箱
        smtp.sendmail(sender, user_email, content.as_string())
        smtp.quit()
        return code
    except ConnectionRefusedError:
        return {'message': '由于目标计算机积极拒绝，无法连接', 'code': 10061}
    except smtplib.SMTPAuthenticationError:
        return {'message': 'user has no permission', 'code': 550}
    # 插入数据到数据库中
    # 获取当前时间
    now_time = int(time.time())
    sql = "insert into email_code (`email`, `e_code`, `date`) values ('%s', '%s', '%s')" % (user_email, code, now_time)
    select(sql)



