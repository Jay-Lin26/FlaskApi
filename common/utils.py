# coding = utf-8
import pymysql
from flask import jsonify
from config import *


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
        if len(result[0]) == 1:
            __list = []
            for i in range(len(result)):
                __email = result[i][0]
                __list.append(__email)
            return __list
        else:
            return list(result)
    except IndexError:
        return []
    except pymysql.err.ProgrammingError:
        return jsonify({'Error': 'An unknown error'})
    except pymysql.err.OperationalError:
        return jsonify({'Error': 'An unknown error'})
