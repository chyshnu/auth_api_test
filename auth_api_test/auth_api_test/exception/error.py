from .base import *


class ERROR_FAULT(ServiceUnavailable503):
    message = "服务器内部错误"
    code = 10001


class WRONG_TOKEN(OK200):
    code = 5000
    message = "非法token"


class PARAMETER_VALIDATE_FAILED(OK200):
    code = 5001
    message = "参数验证未通过"


class ILLEGAL_PARAMETER(OK200):
    code = 5002
    message = "非法的请求参数"


class VERIF_CODE_FREQUENCY_ERROR(OK200):
    code = 5003
    message = "1分钟只能获取1次验证码"


class VERIF_CODE_WRONG(OK200):
    code = 5004
    message = "验证码错误"
