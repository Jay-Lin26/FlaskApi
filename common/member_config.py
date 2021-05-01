# coding = utf-8
import hashlib
import smtplib
import time
from email.mime.text import MIMEText
from random import randint
from smtplib import SMTP_SSL

from flask import jsonify

from common.connection import sql


def randomName():
    u_name = '新用户'
    string_name = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    for i in range(6):
        u_name = u_name + string_name[randint(0, 35)]
    return u_name


def salt():  # 用户盐
    __salt = ''
    int_salt = '1234567890'
    for x in range(6):
        __salt = int_salt[randint(0, 9)] + __salt
    return __salt


def encryption(password, g_salt):  # 密码加密
    # 生成md5对象
    md5 = hashlib.md5(g_salt.encode('utf8'))
    # 对数据加密
    md5.update(password.encode('utf8'))
    # 获取密文
    pwd = md5.hexdigest()
    return pwd


def emailCode():  # 邮箱验证码
    code = ''
    string_code = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    for k in range(6):
        code = string_code[randint(0, 35)] + code
    return code


def sendEmail(user_email):  # 发送邮件
    # 第三方 smtp 服务
    mail_host = 'smtp.163.com'
    mail_user = 'z64666760@163.com'
    password = 'YZYPMEHFIAXZPQLJ'  # 需要使用授权码

    sender = 'z64666760@163.com'
    # 需要发送的邮件内容
    """ 随机验证码 """
    code = emailCode()
    content = MIMEText('您的验证码是：%s' % code)
    content['Subject'] = '注册验证码'  # 邮件主题
    content['From'] = sender  # 发件人
    content['To'] = user_email  # 收件人
    # 连接邮箱服务器；smtp端口是25
    try:
        smtp = SMTP_SSL(mail_host)
        # smtp.connect(mail_host, port=25)
        smtp.login(mail_user, password)  # 登录邮箱
        smtp.sendmail(sender, user_email, content.as_string())
        smtp.quit()
        # 插入数据到数据库中
        # 获取当前时间
        now_time = int(time.time())
        __sql = "insert into email_code (`email`, `email_code`, `send_time`, `code`) values ('%s', '%s', '%s', '%s')" % (
            user_email, '您的验证码是：' + code, now_time, code)
        sql(__sql)
        return code
    except ConnectionRefusedError:
        return jsonify({'message': '由于目标计算机积极拒绝，无法连接', 'code': 10061})
    except smtplib.SMTPAuthenticationError:
        return jsonify({'message': 'user has no permission', 'code': 550})
    except TimeoutError:
        return jsonify({'message': 'Connection timeout', 'code': 10062})
