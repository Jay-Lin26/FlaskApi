# coding = utf-8
# 当前版本号
VERSION = '1.0.1'

# 项目依赖
"""
Flask 1.1.2
Pymysql 0.10.0
flask_CORS 3.0.10
"""
# 数据库地址
DB_HOST = '139.224.63.20'
DB_USER = 'root'
DB_PASSWORD = '123456'
DB_DATABASE = 'flask_v1_pre'

# Flask启动配置
JSONIFY_MIMETYPE = 'application/json'
JSON_SORT_KEYS = False      # 排序
DEBUG = False               # 调试模式
threaded = True             # 多线程

# uwsgi启动
"""
uwsgi --ini uwsgi.ini
uwsgi --stop var/log/uwsgi.pid
uwsgi --reload var/log/uwsgi.pid
"""