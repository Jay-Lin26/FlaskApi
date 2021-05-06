# coding = utf-8
import pymysql
from flask_api.config import *


def dbPerform(sentence):
    try:
        conn = pymysql.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE)
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
        return 'None'
    except pymysql.err.OperationalError:
        return 'None'


def dbPerforms(sentence):
    try:
        conn = pymysql.connect(
            host=DevDatabase.host,
            user=DevDatabase.user,
            password=DevDatabase.password,
            database=DevDatabase.database)
        cursor = conn.cursor()
        cursor.execute(sentence)
        result = cursor.fetchall()
        conn.commit()
        conn.close()
        if len(result[0]) == 1 :
            __list = []
            for i in range(len(result)):
                __email = result[i][0]
                __list.append(__email)
            return __list
        else:
            return result
    except IndexError:
        return []
    except pymysql.err.ProgrammingError:
        return []
    except pymysql.err.OperationalError:
        return []

