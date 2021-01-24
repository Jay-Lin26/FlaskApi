from email.mime.text import MIMEText
from Common.connection import Sql
from random import randint
import hashlib
import smtplib
import time


def Salt():     # 用户盐
    salt = ''
    int_salt = '1234567890'
    for x in range(6):
        salt = int_salt[randint(0, 9)] + salt
    return salt


def encryption(password, salt):  # 密码加密
    # 生成md5对象
    md5 = hashlib.md5(salt.encode('utf8'))
    # 对数据加密
    md5.update(password.encode('utf8'))
    # 获取密文
    pwd = md5.hexdigest()
    print(pwd)
    return pwd, salt


def Email_code():   # 邮箱验证码
    code = ''
    string_code = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    for k in range(6):
        code = string_code[randint(0, 35)] + code
    return code


def send_email(user_email):     # 发送邮件
    # 第三方 smtp 服务
    mail_host = 'smtp.163.com'
    mail_user = 'z64666760@163.com'
    password = 'YZYPMEHFIAXZPQLJ'  # 需要使用授权码

    sender = 'z64666760@163.com'
    # 需要发送的邮件内容
    """ 随机验证码 """
    code = Email_code()
    content = MIMEText('您的验证码是：%s' % code)
    content['Subject'] = '登录验证码'  # 邮件主题
    content['From'] = sender  # 发件人
    content['To'] = user_email  # 收件人
    # 连接邮箱服务器；smtp端口是25
    try:
        smtp = smtplib.SMTP()
        smtp.connect(mail_host, port=25)
        smtp.login(mail_user, password)  # 登录邮箱
        smtp.sendmail(sender, user_email, content.as_string())
        smtp.quit()
        # 插入数据到数据库中
        # 获取当前时间
        now_time = int(time.time())
        sql = "insert into email_code (`email`, `email_code`, `send_time`, `code`) values ('%s', '%s', '%s', '%s')" % (user_email, '您的验证码是：'+code, now_time, code)
        Sql(sql)
        return code
    except ConnectionRefusedError:
        return {'message': '由于目标计算机积极拒绝，无法连接', 'code': 10061}
    except smtplib.SMTPAuthenticationError:
        return {'message': 'user has no permission', 'code': 550}


if __name__ == '__main__':
    encryption('zhou123450', '545384')