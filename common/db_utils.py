# coding = utf-8
import pymysql
from config import DevDatabase


def dbPerform(sentence):
    try:
        conn = pymysql.connect(
            host=DevDatabase.host,
            user=DevDatabase.user,
            password=DevDatabase.password,
            database=DevDatabase.database)
        cursor = conn.cursor()
        __sql = sentence
        cursor.execute(__sql)
        result = cursor.fetchall()
        conn.commit()
        conn.close()
        return result
    except IndexError:
        return {'message': ' select IndexError '}
    except pymysql.err.OperationalError:
        return {'message': ' select OperationalError'}
