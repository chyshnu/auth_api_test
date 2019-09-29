import random
import time
import uuid
import os
import base64
import hashlib
from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse
from Crypto.Cipher import AES


def json_response(message, data=[], code=0):
    return JsonResponse(
        {
            'code': 0,
            'msg': message,
            'data': data
        }
    )


def make_vcode():
    """发送验证码"""
    # TODO: 接入短信发送API
    vcode = str(random.randrange(1000, 9999))  # 随机4位验证码
    print("验证码：" + vcode)
    return vcode


def validate_vcode(mobile, vcode):
    """验证码校验"""
    if vcode == cache.get(mobile):
        cache.delete(mobile)    # 登录成功后，删除缓存中的验证码
        return True
    return False


def timestamp():
    """获取13位时间戳"""
    return str(int(time.time() * 1000))


def make_token():
    """生成40位Token值"""
    token = hashlib.sha1(os.urandom(24)).hexdigest()
    # print(type(token))
    return token
