# coding=GBK
import string
import random
import xlrd
import xlwt
import os
import django
import sys
from xlutils.copy import copy
from UserProfile.models import User


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "OnlineJudge.settings")  # project_name 项目名称
django.setup()


def get_pwd(size=8, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for i in range(size))


filename = 'E:\\文件仓库\\2018年大一新生C语言考试报名表.xls'
cnt_rd = 0
pwd_list = []


def register():
    data = xlrd.open_workbook(filename)
    table = data.sheet_by_name(u'Sheet1')   # 通过名称获取
    row = table.nrows
    col = table.ncols
    for i in range(1, row):
        j = 0
        stu_username = str(int(table.cell(i, j+2).value)).strip()
        stu_class = table.cell(i, j+1).value.strip()
        stu_no = stu_username
        stu_pwd = get_pwd()
        stu = User.objects.create_user(username=stu_username, email='',
                                       password=stu_pwd, myClass=stu_class, stuId=stu_no)
        if stu is not None:
            global cnt_rd, pwd_list
            pwd_list.append(stu_pwd)
            cnt_rd += 1
        else:
            print('第 %d 个用户注册失败' % i)
    print('现在已经成功注册了 %d 个用户' % cnt_rd)


def save_pwd():
    global pwd_list
    rb = xlrd.open_workbook(filename)
    wb = copy(rb)
    sheet = wb.get_sheet(0)
    row = wb.nrows
    col = wb.ncols
    j = 0
    for i in range(1, row):
        sheet.write(i, col, pwd_list[j])
        j += 1
    os.remove(filename)
    wb.save(filename)


def start():
    register()
    save_pwd()
    print('注册完成！')


start()
