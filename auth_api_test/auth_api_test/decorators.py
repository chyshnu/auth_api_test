import functools
import time

from django.core.cache import cache
from auth_api_test.exception.base import ApiException
from auth_api_test.exception.error import *
from auth_api_test.api.crypt import BizMsgCrypt
from django.conf import settings


def check_token(function):
    """检查用户token是否正常"""

    def _inner(request, *args, **kwargs):

        # 获取Request请求Headers中的token字段
        token = request.headers.get('Access-Token')
        if not token:
            # 没有token参数，抛出异常
            raise ApiException(Parameter_Missing, suffix='token')
        user = cache.get(token)
        if user:
            pass
        else:
            # 缓存中找不到token，抛出异常
            raise ApiException(Wrong_Token)

        return function(request, *args, **kwargs)

    return _inner


def verify_url(function):
    """验证url"""
    def _inner(request, *args, **kwargs):

        # 获取Request请求Headers中的token字段
        token = request.headers.get('Access-Token')
        ts = request.p('timestamp')
        nonce = request.p('nonce')
        encrypt = request.p('encrypt')
        signature = request.p('signature')
        if not BizMsgCrypt.verify_url(signature, token, ts, nonce, encrypt, settings.SALT):
            # 校验失败抛出异常
            raise ApiException(Wrong_Url)

        return function(request, *args, **kwargs)

    return _inner


def timeit(function):
    """计算视图相应时间"""

    def timed(*args, **kw):
        ts = time.time()
        result = function(*args, **kw)
        te = time.time()
        print('%r (%r, %r) %2.3f sec' % (function.__name__, args, kw, te - ts))
        return result

    return timed


def check_params(param_validate_dict):
    """请求参数验证器"""

    def decorator(function):
        @functools.wraps(function)
        def _inner(request, *args, **kwargs):
            # params_dict = json.loads(request.body)  # type(params_dict)  -->  <class 'dict'>
            for k, v in param_validate_dict.items():
                verify_field_value = request.p(k)

                # 如果应当验证的参数在请求参数中不存在，抛出非法请求参数异常
                if not verify_field_value:
                    raise ApiException(Parameter_Missing, suffix=k)

                v.set_request(request)  # 将请求传入验证对象

                # 如果请求参数验证未通过，直接抛出异常
                v.check_field(verify_field_value)

            return function(request, *args, **kwargs)

        return _inner
    return decorator
