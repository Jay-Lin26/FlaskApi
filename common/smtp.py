# coding = utf-8
import smtplib
import time
from email.header import Header
from email.mime.text import MIMEText
from smtplib import SMTP_SSL

from flask import jsonify

from common.edm import *
from common.utils import dbPerform, randomNumber
from config import *


def sendEmail(accept_email):  # 发送邮件
    verification_sql = """
                            INSERT INTO
                                verification_log (`email`, `message`, `send_time`, `verification_code`)
                            VALUES
                                ('{}', '{}', '{}', '{}')
                       """
    # 需要发送的邮件内容
    code = randomNumber(6)
    content = MIMEText('%s' % edm_html.format(message=code), 'html', 'utf-8')
    content['Subject'] = Header('验证码', 'utf-8').encode()  # 邮件主题
    content['From'] = 'iBlogs <noreply@iblogs.ltd>'  # 发件人
    content['To'] = accept_email  # 收件人
    # 连接邮箱服务器；smtp端口是25
    try:
        smtp = SMTP_SSL(SMTP_HOST, PORT)
        smtp.login(SMTP_USER, SECRET_KEY)  # 登录邮箱
        smtp.sendmail(SMTP_USER, accept_email, content.as_string())
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
