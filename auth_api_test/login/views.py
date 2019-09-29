from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from django.conf import settings
# from auth_api_test.validate import VT
from auth_api_test.decorators import check_token, timeit, check_params
from auth_api_test.validate import *


# Create your views here.
def json_response_test(request):
    return JsonResponse(
        {
            'code': 0,
            'msg': settings.MY_CONF,
            'data': []
        }, status=200
    )


def session_test(request):
    return JsonResponse(
        {
            'code': 0,
            'msg': 'OK',
            'data': []
        }, status=200
    )


@require_POST
@check_token
@check_params({
    'username': AccountValidator('用户名'),
    'password': PasswordValidator('密码')
})
# @timeit
def user_login(request):
    print('In View')
    # av = AccountValidate('用户名')
    # print(av.check_field(request.POST.get('username', None)))
    return JsonResponse(
        {
            'code': 0,
            'msg': '登录成功',
            'data': request.POST
        }
    )

