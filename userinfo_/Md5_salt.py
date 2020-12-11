import hashlib


""" 密码加密"""


def encryption(password):
    # 生成md5对象
    md5 = hashlib.md5(b'zhou')
    # 对数据加密
    md5.update(password.encode('utf-8'))
    # 获取密文
    pwd = md5.hexdigest()
    return pwd

