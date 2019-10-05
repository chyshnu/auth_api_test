from django.views.decorators.http import require_POST, require_GET
from auth_api_test.decorators import check_token, check_params, verify_url
from auth_api_test.validate import *
from auth_api_test.api.utils import *
from auth_api_test.api.crypt import *
from django.conf import settings
from .models import User, UserInfo


# @require_POST
@check_params({'timestamp': NumberValidator('时间戳', 10), 'nonce': NumberValidator('随机串', 8),
               'signature': AncuscValidator('签名', 40), 'encrypt': AncuscValidator('密文', 1, 512)})   # :TODO 请求长度修改
@check_token
@verify_url
def test_json(request):
    encrpyt_text = request.p('encrypt')
    token = request.headers.get('Access-Token')

    bmc = BizMsgCrypt(token, settings.SECRET_KEY, settings.SALT)
    plain_json = bmc.decryptMsg(encrpyt_text)
    print(plain_json)
    print(plain_json['ToUserName'])

    # ----------- 加密 -----------

    # plain_text = 'Hello China, Hello World!'
    plain_text = '{ "ToUserName": "wx5823bf96d3bd56c7", "FromUserName": :mycreate", "CreateTime": 1409659813, ' \
                 '"MsgType": "text", "Content": "hello", "MsgId": 4561255354251345929, "AgentID": 218} '
    cipher_json = bmc.encryptMsg(plain_text)
    # print(ciphertext)

    return JsonResponse(
        {
            'code': OK[0],
            'msg': OK[1],
            'data': cipher_json
        }
    )


@require_POST
@check_params({'username': UsernameValidator('用户名'), 'password': PasswordValidator('密码'),
               'email': EmailValidator('邮箱'), 'mobile': MobileValidator('手机号')})
@check_token
# @timeit
def login(request):
    username = request.p('username')
    password = request.p('password')
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
    mobile = request.p('mobile')

    # 检测用户是否已存在
    user = User.mobile_is_exist(mobile)
    if user:
        if not user.status:  # 用户被禁用抛出异常
            raise ApiException(User_Forbidden)
    else:
        # 创建新用户
        user = User(username=mobile, mobile=mobile)
        user.save()
        ui = UserInfo(user=user)
        ui.save()

    token = make_token()
    refresh_token = make_token()
    expires = settings.TOKEN_EXPIRES

    # token放入缓存
    cache.set(token, user, expires)
    # TODO: refresh_token 放入缓存绑定access_token

    return json_response('登录成功', {
        'access_token': token,
        'refresh_token': refresh_token,
        'expires_in': expires   # - 7140 + 30
    })


@require_POST
@check_params({'mobile': MobileValidator('手机号')})
def send_vcode(request):
    """获取验证码"""
    mobile = request.p('mobile')

    # 如果缓存中有验证码，说明1分钟内重复请求了
    if cache.get(mobile):
        raise ApiException(Verify_Code_Frequency_Error)
    else:
        v_code = make_vcode()
        cache.set(mobile, v_code, 60)

    return json_response('验证码发送成功', {'vcode': v_code} if settings.DEBUG else [])
