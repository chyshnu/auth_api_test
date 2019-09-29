import functools
import time, json

from auth_api_test.exception.error import *


def check_token(function):
    """检查用户token是否正常"""

    def _inner(request, *args, **kwargs):
        token = request.POST.get('token', None)
        # req_dict = json.loads(request.body)
        # token = req_dict.get('token', None)
        if not token:
            raise WRONG_TOKEN()
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
            params_dict = dict(getattr(request, request.method, None))
            # params_dict = json.loads(request.body)  # type(params_dict)  -->  <class 'dict'>
            # print(params_dict)
            for k, v in param_validate_dict.items():
                verify_field_value = params_dict.get(k, None)

                # 如果应当验证的参数在请求参数中不存在，抛出非法请求参数异常
                if not verify_field_value:
                    raise ILLEGAL_PARAMETER({
                        'field': k,
                        'field_desc': v.verify_field_desc,
                        'hint': '请求参数不存在'
                    })

                # 如果请求参数验证未通过，抛出参数验证未通过异常
                res, hint = v.check_field(verify_field_value[0])
                if not res:
                    raise PARAMETER_VALIDATE_FAILED({
                        'field': k,
                        'field_desc': v.verify_field_desc,
                        'hint': hint
                    })

            return function(request, *args, **kwargs)

        return _inner
    return decorator
