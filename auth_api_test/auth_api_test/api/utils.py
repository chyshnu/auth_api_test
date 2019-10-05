import random
import time
import uuid
import os
import base64
import hashlib
from django.core.cache import cache
from django.http import JsonResponse
from Crypto.Cipher import AES
from auth_api_test.exception.base import ApiException
from auth_api_test.exception.error import *


def json_response(message, data='', code=OK[0]):
    return JsonResponse(
        {
            'code': code,
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


def make_timestamp():
    """获取13位时间戳"""
    return str(int(time.time()))


def make_nonce():
    """获取8位随机串"""
    return str(random.randint(10000000, 99999999))


def make_token():
    """生成40位Token值"""
    token = hashlib.sha1(os.urandom(24)).hexdigest()
    return token


# class TokenInfo:
#
#     def __init__(self, userid, appid, token, refresh_token, time_base):
#         self.userid = userid
#         self.appid = appid
#         self.token = token
#         self.refresh_token = refresh_token
#         self.time_base = time_base

