from django.db import models


class User(models.Model):
    username = models.CharField("用户名", max_length=16, unique=True)
    userpic = models.CharField("头像", max_length=128, null=True, blank=True)
    password = models.CharField("密码", max_length=128, null=True, blank=True)
    mobile = models.CharField("手机", max_length=16, unique=True)
    email = models.CharField("邮箱", max_length=50, null=True, blank=True)
    status = models.BooleanField("状态", default=True)
    c_time = models.DateTimeField("加入时间", auto_now_add=True)

    @classmethod
    def mobile_is_exist(cls, mobile):
        return cls.objects.filter(mobile=mobile).first()


class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sex = models.BooleanField("性别", null=True, blank=True)  # True: 男   False: 女
    birthday = models.DateField("生日", null=True, blank=True)
    home_city = models.CharField("城市", max_length=32, null=True, blank=True)
    profile = models.CharField("个人简介", max_length=256, null=True, blank=True)


