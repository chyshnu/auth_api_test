from django.views.decorators.http import require_POST
from auth_api_test.decorators import check_token, timeit, check_params
from auth_api_test.validate import *
from auth_api_test.exception.error import *
from auth_api_test.utils import *


def json_response_test(request):
    return JsonResponse(
        {
            'code': 0,
            'msg': settings.SALT,
            'data': make_token()
        }
    )


@require_POST
@check_params({
    'username': UsernameValidator('用户名'),
    'password': PasswordValidator('密码'),
    'email': EmailValidator('邮箱'),
    'mobile': MobileValidator('手机号')
})
@check_token
# @timeit
def login(request):
    username = request.POST['username']
    password = request.POST['password']
    print(request.content_type)
    return JsonResponse(
        {
            'code': 0,
            'msg': '登录成功',
            'data': request.POST
        }
    )


@require_POST
@check_params({'mobile': MobileValidator('手机号'), 'vcode': VcodeValidator('验证码')})
def mobile_login(request):
    """手机号码登录"""
    mobile = request.POST.get('mobile')
    vcode = request.POST.get('vcode')

    if validate_vcode(mobile, vcode):
        # TODO: 判断用户是否存在，创建新用户
        # TODO: 生成Token
        return json_response('登录成功', {
            'token': '123123',
            'refresh_token': '999999'
        })
    else:
        raise VERIF_CODE_WRONG()


@require_POST
@check_params({'mobile': MobileValidator('手机号')})
def send_vcode(request):
    """获取验证码"""
    mobile = request.POST.get('mobile')

    # 如果缓存中有验证码，说明1分钟内重复请求了
    if cache.get(mobile):
        raise VERIF_CODE_FREQUENCY_ERROR()
    else:
        v_code = make_vcode()
        cache.set(mobile, v_code, 60)
    return json_response('验证码发送成功')
