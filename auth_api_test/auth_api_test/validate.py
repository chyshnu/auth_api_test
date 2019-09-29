import re

# 验证类型
VT = {
    'ACCOUNT': (r'^[a-zA-Z][a-zA-Z0-9\_]{4,15}$', '字母开头，长度5-16位，允许字母数字及下划线'),
    'PASSWORD': (r'^.*(?=.{8,16})(?=.*\d)(?=.*[A-Z]{1,})(?=.*[a-z]{1,}).*$', '长度8-16位，必须包含数字及大小写字母'),
}


class BaseValidator:
    """验证器基类"""
    def __init__(self, pattern, pattern_desc, verify_field_desc):
        """初始化正则模式、正则描述以及即将验证的字段描述"""
        self.__pattern = pattern
        self.pattern_desc = pattern_desc
        self.verify_field_desc = verify_field_desc

    def check_field(self, verify_field_value):
        """验证字段"""
        if re.match(self.__pattern, verify_field_value):
            return True
        else:
            return False


class AccountValidator(BaseValidator):
    """账号验证器"""
    def __init__(self, verify_field_name):
        BaseValidator.__init__(self, VT['ACCOUNT'][0], VT['ACCOUNT'][1], verify_field_name)


class PasswordValidator(BaseValidator):
    """密码验证器"""
    def __init__(self, verify_field_name):
        BaseValidator.__init__(self, VT['PASSWORD'][0], VT['PASSWORD'][1], verify_field_name)


