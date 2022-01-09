# coding = utf-8
import hashlib
import time
from random import randint

import pymysql
from flask import jsonify, request

from config import *


# 数据库操作——单个字段查询{ 也可直接进行其它操作 }
def dbPerform(sentence):
    try:
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_DATABASE)
        cursor = conn.cursor()
        cursor.execute(sentence)
        result = cursor.fetchone()
        conn.commit()
        conn.close()
        if result is None:
            return 'None'
        return list(result)[0]
    except IndexError:
        return 'None'
    except pymysql.err.ProgrammingError:
        return jsonify({'Error': 'An unknown error'})
    except pymysql.err.OperationalError:
        return jsonify({'Error': 'An unknown error'})


# 数据库查询——多条数多字段查询
def dbPerforms(sentence):
    try:
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_DATABASE)
        cursor = conn.cursor()
        cursor.execute(sentence)
        result = cursor.fetchall()
        conn.commit()
        conn.close()
        return list(result)
    except IndexError:
        return []
    except pymysql.err.ProgrammingError:
        return jsonify({'Error': 'An unknown error'})
    except pymysql.err.OperationalError:
        return jsonify({'Error': 'An unknown error'})


# 随机数
def randomNumber(length=6):
    number = ''
    six_number = '1234567890'
    for i in range(int(length)):
        number = six_number[randint(0, 9)] + number
    return number


# 时间戳转为年月日格式
def changeTime(timestamp):
    __time = time.localtime(int(timestamp))
    cst_time = time.strftime('%Y-%m-%d', __time)
    return cst_time


def randomName():
    u_name = '新用户'
    string_name = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    for i in range(6):
        u_name = u_name + string_name[randint(0, 35)]
    return u_name


def encryption(password, g_salt):  # 密码加密
    # 生成md5对象
    md5 = hashlib.md5(g_salt.encode('utf8'))
    # 对数据加密
    md5.update(password.encode('utf8'))
    # 获取密文
    pwd = md5.hexdigest()
    return pwd


def loginRequired(func):
    def inner():
        token = request.headers.get('access_token')
        if token is None or token == ' ':
            return jsonify(code=4002, msg='Please login first')
        else:
            return func()
    return inner
