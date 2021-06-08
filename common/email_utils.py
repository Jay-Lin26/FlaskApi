# coding = utf-8
import smtplib
import time
from email.mime.text import MIMEText
from email.header import Header
from random import randint
from smtplib import SMTP_SSL

from flask import jsonify

from common.db_utils import dbPerform
from common.edm import *


def emailCode():  # 邮箱验证码
    code = ''
    string_code = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    for k in range(6):
        code = string_code[randint(0, 35)] + code
    return code


def sendEmail(accept_email):  # 发送邮件
    # 第三方 smtp 服务
    mail_host = 'smtp.163.com'
    mail_user = 'z64666760@163.com'
    password = 'YZYPMEHFIAXZPQLJ'  # 需要使用授权码
    verification_sql = """
        INSERT INTO
            verification_log (`email`, `message`, `send_time`, `verification_code`)
        VALUES
            ('{}', '{}', '{}', '{}')
    """
    # 需要发送的邮件内容
    """ 随机验证码 """
    code = emailCode()
    content = MIMEText('%s' % edm_html.format(message=code), 'html', 'utf-8')
    content['Subject'] = Header('邮箱验证码', 'utf-8').encode()  # 邮件主题
    content['From'] = Header('iBlogs<noreply@iBlogs.com>', 'utf-8').encode()  # 发件人
    content['To'] = accept_email  # 收件人
    # 连接邮箱服务器；smtp端口是25
    try:
        smtp = SMTP_SSL(mail_host)
        smtp.login(mail_user, password)  # 登录邮箱
        smtp.sendmail(mail_user, accept_email, content.as_string())
        smtp.quit()
        now_time = int(time.time())
        dbPerform(verification_sql.format(accept_email, '您的验证码是：' + code, now_time, code))
        return code
    except ConnectionRefusedError:
        return jsonify({'code': 1101, 'message': 'Connection timeout'})
    except smtplib.SMTPAuthenticationError:
        return jsonify({'code': 1102, 'message': 'User has no permission'})
    except TimeoutError:
        return jsonify({'code': 1103, 'message': 'Connection timeout'})
    except smtplib.SMTPRecipientsRefused:
        return jsonify({'code': 1104, 'message': 'Connection timeout'})
