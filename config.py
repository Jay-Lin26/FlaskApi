# coding = utf-8
# 数据库地址
class DevDatabase:
    host = '47.100.164.202'
    user = 'root'
    password = '123456'
    database = 'Testcases'


# Flask启动配置
JSONIFY_MIMETYPE = 'application/json'
JSON_SORT_KEYS = False
DEBUG = True


'''
default_config =
    {
        "ENV": None,                    #虚拟环境，当前项目运行环境
        "DEBUG": None,                  #debug模式的设置,开发环境用，自动重启项目，日志级别低，报错在前端显示具体代码
        "TESTING": False,               #测试模式的设置，无限接近线上环境，不会重启项目，日志级别较高，不会在前端显示错误代码
        "PROPAGATE_EXCEPTIONS": None,
        "PRESERVE_CONTEXT_ON_EXCEPTION": None,
        "SECRET_KEY": None,             #session秘钥配置
        "PERMANENT_SESSION_LIFETIME": timedelta(days=31),   #session有效期时间的设置
        "USE_X_SENDFILE": False,    
        "SERVER_NAME": None,            #主机名设置
        "APPLICATION_ROOT": "/",        #应用根目录配置
        "SESSION_COOKIE_NAME": "session",   #cookies中存储的session字符串的键
        "SESSION_COOKIE_DOMAIN": None,      #session作用域
        "SESSION_COOKIE_PATH": None,        #session作用的请求路径
        "SESSION_COOKIE_HTTPONLY": True,    #session是否只支持http请求方式
        "SESSION_COOKIE_SECURE": False,     #session安全配置
        "SESSION_COOKIE_SAMESITE": None,
        "SESSION_REFRESH_EACH_REQUEST": True,
        "MAX_CONTENT_LENGTH": None,
        "SEND_FILE_MAX_AGE_DEFAULT": timedelta(hours=12),
        "TRAP_BAD_REQUEST_ERRORS": None,
        "TRAP_HTTP_EXCEPTIONS": False,
        "EXPLAIN_TEMPLATE_LOADING": False,
        "PREFERRED_URL_SCHEME": "http",
        "JSON_AS_ASCII": True,
        "JSON_SORT_KEYS": True,
        "JSONIFY_PRETTYPRINT_REGULAR": False,
        "JSONIFY_MIMETYPE": "application/json",     #设置jsonify响应时返回的contentype类型
        "TEMPLATES_AUTO_RELOAD": None,
        "MAX_COOKIE_SIZE": 4093,

}'''
