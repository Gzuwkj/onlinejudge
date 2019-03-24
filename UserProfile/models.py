from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    GENDER_CHOICE = (('男', '男'), ('女', '女'))
    USER_AUTHORITY_CHOSE = (('超级管理员', '超级管理员'), ('管理员', '管理员'), ('用户', '用户'))
    # nickname = models.CharField(max_length=50, blank=True)
    # gender = models.CharField(max_length=4, choices=GENDER_CHOICE, null=True, blank=True)                # 性别
    school = models.CharField(max_length=30, default="贵州大学", blank=True)                              # 学校
    major = models.CharField(max_length=10, blank=True)                                                    # 专业
    myClass = models.CharField(max_length=15, blank=True)                                                  # 班级
    stuId = models.CharField(max_length=20, blank=True)                                                    # 学号
    headImage = models.ImageField(upload_to='headImage', default="medie/headimage/1.jpg")               # 头像
    synopsis = models.TextField(default="这个人很懒，什么都没有写...", blank=True)                        # 简介
    tel = models.CharField(max_length=11, blank=True)                                                     # 手机号
    authority = models.CharField(max_length=5, choices=USER_AUTHORITY_CHOSE, default="用户", blank=True)  # 用户权限

    class Meta(AbstractUser.Meta):
        pass
