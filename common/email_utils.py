# coding = utf-8
import smtplib
import time
from email.mime.text import MIMEText
from random import randint
from smtplib import SMTP_SSL

from flask import jsonify

from common.db_utils import dbPerform


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
    verification_sql = """
        INSERT INTO
            email_code (`email`, `email_code`, `send_time`, `code`)
        VALUES
            ('{}', '{}', '{}', '{}')
    """
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
        smtp.login(mail_user, password)  # 登录邮箱
        smtp.sendmail(sender, user_email, content.as_string())
        smtp.quit()
        now_time = int(time.time())
        dbPerform(verification_sql.format(user_email, '您的验证码是：' + code, now_time, code))
        return code
    except ConnectionRefusedError:
        return jsonify({'code': 1101, 'message': 'Connection timeout'})
    except smtplib.SMTPAuthenticationError:
        return jsonify({'code': 1102, 'message': 'User has no permission'})
    except TimeoutError:
        return jsonify({'code': 1103, 'message': 'Connection timeout'})
