class ApiException(Exception):
    """自定义异常类"""
    def __init__(self, exp_type, prefix=None, suffix=None, custom_msg=None, status_code=200):
        self.code = exp_type[0]
        self.message = exp_type[1]

        # 使用自定义message
        if custom_msg:
            self.message = custom_msg

        # 为message添加前缀
        if prefix:
            self.message = prefix + self.message

        # 为message添加后缀
        if suffix:
            self.message = self.message + suffix

        # response状态码
        self.status_code = status_code

