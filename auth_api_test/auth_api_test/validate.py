import re
from auth_api_test.exception.base import ApiException
from auth_api_test.exception.error import *
from django.core.cache import cache

# 验证类型
VT = {
    'USERNAME': (r'^[a-zA-Z][a-zA-Z0-9\_]{4,15}$', '字母开头，长度5-16位，允许字母数字及下划线'),
    'PASSWORD': (r'^.*(?=.{8,16})(?=.*\d)(?=.*[A-Z]{1,})(?=.*[a-z]{1,}).*$', '长度8-16位，必须包含数字及大小写字母'),
    'MOBILE': (r'^1(3|4|5|6|7|8|9)\d{9}$', '11位手机号码'),
    'EMAIL': (r'^[A-Za-z\d]+([-_.][A-Za-z\d]+)*@([A-Za-z\d]+[-.])+[A-Za-z\d]{2,4}$',
              "前缀、后缀不以'_'、'-'、'.'结尾，后缀结尾2-4位"),
    'NUMBER': (r'^[0-9]{%d,%d}$', '%d-%d位数字串'),
    'ANCUSC': (r'^(.*){%d,%d}$', '长度%d-%d位，包含指定长度的小写字母及数字字符')    # TODO: 修改验证规则
}


class BaseValidator:
    """验证器基类"""
    __request = None

    def __init__(self, pattern, pattern_desc, verify_field_desc):
        """初始化正则模式、正则描述以及即将验证的字段描述"""
        self.__pattern = pattern
        self.pattern_desc = pattern_desc
        self.verify_field_desc = verify_field_desc

    def custom_check(self, verify_field_value):
        """
        自定义验证字段

        Args:
            verify_field_value: 待验证的字段值
        Returns:
            校验不通过，抛出异常；校验通过，无返回结果
        """
        pass

    def check_field(self, verify_field_value):
        """
        正则表达式验证字段

        Args:
            verify_field_value: 待验证的字段值
        Returns:
            校验不通过，抛出异常；校验通过，无返回结果
        """
        if not re.match(self.__pattern, verify_field_value):
            raise ApiException(Parameter_Validate_Failed, prefix=self.verify_field_desc)
        # 调用自定义验证方法
        self.custom_check(verify_field_value)

    def set_request(self, request):
        """传入request对象"""
        self.__request = request

    def get_request(self):
        """获取request对象"""
        return self.__request


class UsernameValidator(BaseValidator):
    """账号验证器"""
    def __init__(self, verify_field_name):
        BaseValidator.__init__(self, VT['USERNAME'][0], VT['USERNAME'][1], verify_field_name)


class PasswordValidator(BaseValidator):
    """密码验证器"""
    def __init__(self, verify_field_name):
        BaseValidator.__init__(self, VT['PASSWORD'][0], VT['PASSWORD'][1], verify_field_name)


class MobileValidator(BaseValidator):
    """手机号码验证器"""
    def __init__(self, verify_field_name):
        BaseValidator.__init__(self, VT['MOBILE'][0], VT['MOBILE'][1], verify_field_name)


class EmailValidator(BaseValidator):
    """邮箱地址验证器"""
    def __init__(self, verify_field_name):
        BaseValidator.__init__(self, VT['EMAIL'][0], VT['EMAIL'][1], verify_field_name)

    def custom_check(self, verify_field_value):
        if len(verify_field_value) > 50:
            raise ApiException(Parameter_Validate_Failed, prefix=self.verify_field_desc, custom_msg='长度不能超过50位')


class VcodeValidator(BaseValidator):
    """验证码验证器"""
    def __init__(self, verify_field_name):
        BaseValidator.__init__(self, VT['NUMBER'][0] % (4, 4), VT['NUMBER'][1] % (4, 4), verify_field_name)

    def custom_check(self, verify_field_value):
        req = self.get_request()
        mobile = req.p('mobile')
        vcode = verify_field_value
        cached_vcode = cache.get(mobile)

        if not cached_vcode:
            raise ApiException(Verify_Code_Resend)
        if not (vcode == cached_vcode):
            raise ApiException(Verify_Code_Wrong)


class NumberValidator(BaseValidator):
    """数字串验证器"""
    def __init__(self, verify_field_name, min_length=1, max_length=None):
        if max_length:
            if max_length < min_length:
                min_length = max_length
        else:
            max_length = min_length
        BaseValidator.__init__(self, VT['NUMBER'][0] % (min_length, max_length),
                               VT['NUMBER'][1] % (min_length, max_length),
                               verify_field_name)


class AncuscValidator(BaseValidator):
    """常用密文字符串验证器"""
    def __init__(self, verify_field_name, min_length=1, max_length=None):
        if max_length:
            if max_length < min_length:
                min_length = max_length
        else:
            max_length = min_length
        BaseValidator.__init__(self, VT['ANCUSC'][0] % (min_length, max_length),
                               VT['ANCUSC'][1] % (min_length, max_length),
                               verify_field_name)
