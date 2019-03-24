from django.db import models
import os

POWER_CHOSE = (('公开', '公开'), ('隐藏', '隐藏'))
LANGUAGE_CHOICE = (('C', 'C'), ('C++', 'C++'), ('Java', 'Java'), ('Python', 'Python'))


def save_standard_input(instance, filename):
    return os.path.join(str(instance), '1.in')


def save_standard_output(instance, filename):
    return os.path.join(str(instance), '1.out')


class Problem(models.Model):                                                                          # 问题类
    no = models.IntegerField(primary_key=True)                                                        # 题目编号
    title = models.CharField(max_length=20, unique=True)                                              # 标题
    content = models.TextField(blank=True)                                                            # 内容
    myInput = models.TextField(blank=True)                                                            # 输入
    myOutput = models.TextField(blank=True)                                                           # 输出
    time = models.IntegerField(blank=True, default=1000)                                              # 运行时间
    memory = models.IntegerField(blank=True, default=256)                                             # 运行内存
    sampleInput = models.TextField(blank=True, default='')                                            # 样列输入
    sampleOutput = models.TextField(blank=True, default='')                                           # 样列输出
    standardInput = models.FileField(upload_to=save_standard_input, blank=True)                       # 标准输入
    standardOutput = models.FileField(upload_to=save_standard_output, blank=True)                     # 标准输出
    tips = models.TextField(blank=True)                                                               # 提示
    probSource = models.CharField(max_length=10, blank=True)                                          # 题目来源
    classification = models.CharField(max_length=10, blank=True)                                      # 分类
    probAuthority = models.CharField(default='公开', choices=POWER_CHOSE, max_length=2)                # 权限
    weight = models.IntegerField(default=100)                                                          # 分数

    def __str__(self):
        return str(self.no)


class ProblemCode(models.Model):                                                                      # 用户题库提交的代码
    userName = models.CharField(max_length=30, blank=True)                                            # 用户名
    probID = models.IntegerField()                                                                    # 题目编号
    content = models.TextField(blank=True)                                                           # 提交代码
    runID = models.AutoField(primary_key=True)                                                       # 运行编号
    result = models.CharField(max_length=2, default='0', blank=True)                                # 运行结果
    time = models.IntegerField(blank=True, default=0)                                                # 运行时间
    memory = models.IntegerField(blank=True, default=0)                                              # 运行内存
    language = models.CharField(default='C++', blank=True, max_length=9, choices=LANGUAGE_CHOICE)   # 语言
    subTime = models.DateTimeField(auto_now=True)                                                   # 提交时间

    def __str__(self):
        return self.problemId
