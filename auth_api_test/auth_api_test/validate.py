import re
# from abc import ABCMeta, abstractmethod

# 验证类型
VT = {
    'USERNAME': (r'^[a-zA-Z][a-zA-Z0-9\_]{4,15}$',
                 '字母开头，长度5-16位，允许字母数字及下划线'),
    'PASSWORD': (r'^.*(?=.{8,16})(?=.*\d)(?=.*[A-Z]{1,})(?=.*[a-z]{1,}).*$',
                 '长度8-16位，必须包含数字及大小写字母'),
    'MOBILE': (r'^1(3|4|5|6|7|8|9)\d{9}$',
               '11位手机号码'),
    'EMAIL': (r'^[A-Za-z\d]+([-_.][A-Za-z\d]+)*@([A-Za-z\d]+[-.])+[A-Za-z\d]{2,4}$',
              "前缀、后缀不以'_'、'-'、'.'结尾，后缀结尾2-4位"),
    'VCODE': (r'^\d{4}$',
              '验证码错误'),
}


class BaseValidator:
    """验证器基类"""
    # __metaclass__ = ABCMeta

    def __init__(self, pattern, pattern_desc, verify_field_desc):
        """初始化正则模式、正则描述以及即将验证的字段描述"""
        self.__pattern = pattern
        self.pattern_desc = pattern_desc
        self.verify_field_desc = verify_field_desc

    def custom_check(self, verify_field_value):
        """自定义验证字段"""
        return True, ''

    def check_field(self, verify_field_value):
        """正则表达式验证字段"""
        if not re.match(self.__pattern, verify_field_value):
            return False, self.pattern_desc
        return self.custom_check(verify_field_value)    # 调用自定义验证方法


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
            return False, '长度不能超过50位'
        return True, ''


class VcodeValidator(BaseValidator):
    """验证码验证器"""
    def __init__(self, verify_field_name):
        BaseValidator.__init__(self, VT['VCODE'][0], VT['VCODE'][1], verify_field_name)

