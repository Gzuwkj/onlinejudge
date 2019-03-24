from django.shortcuts import render

from django.shortcuts import render,render_to_response
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib import auth
from django.template import RequestContext
import time

from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from UserProfile.models import User
from django.views.decorators.csrf import csrf_exempt
# 第四个是auth中用户权限有关的类。auth可以设置每个用户的权限。

from Contest.models import MatchSubmit
# Create your views here.

# -*- coding: utf-8 -*-


def index(request):
    username = str(request.user)
    if username == 'AnonymousUser':
        return HttpResponseRedirect("/login/")
    user = User.objects.get(username=username)
    return render(request, 'index.html', {'user': user})


def userinfo_view(request, uid):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        pwd = request.POST.get('pwd', '')
        repwd = request.POST.get('repwd', '')
        email = request.POST.get('email', '')
        tel = request.POST.get('tel', '')
        synopsis = request.POST.get('synopsis', '')
        headImage = request.FILES.get('headImage', '')
        if headImage != '':
            with open(headImage.name, 'wb') as f:
                for line in headImage:
                    f.write(line)
        try:
            user = User.objects.get(id=str(uid))
        except:
            return HttpResponseRedirect("/index/")
        if name != '':
            user.username = name
        if email != '':
            user.email = email
        if tel != '':
            user.tel = tel
        if synopsis != '':
            user.synopsis = synopsis
        if headImage != '':
            user.headImage = headImage
        user.save()
        user_name = user.username
        submit_time = MatchSubmit.objects.filter(userName=user_name).count()
        try_time = MatchSubmit.objects.values('probID').distinct().count()
        right_time = MatchSubmit.objects.filter(userName=user_name, result=1).count()
        return render(request, 'userinfo.html', locals())
    else:
        user_name = request.user
        if str(user_name) == 'AnonymousUser':
            return HttpResponseRedirect("/login/?next=/index/")
        try:
            user = User.objects.get(id=str(uid))
        except:
            return HttpResponseRedirect("/index/")
        user_name = user.username
        submit_time = MatchSubmit.objects.filter(userName=user_name).count()
        try_time = MatchSubmit.objects.values('probID').distinct().count()
        right_time = MatchSubmit.objects.filter(userName=user_name, result=1).count()
        return render(request, 'userinfo.html', locals())

# 注册


def register_view(req):
    if req.session.get('is_login', None):
        return HttpResponseRedirect("/index/")
    if req.method == 'POST':
        user_pwd = req.POST.get("password", "")
        user_repwd = req.POST.get("repassword", "")
        if user_pwd != user_repwd:
            user_password_error = True
            return render(req, 'register.html', {'user_password_error': user_password_error})
        user_name = req.POST.get("username", "")
        if User.objects.filter(username=user_name).count():
            user_repeat = True
            return render(req, 'register.html', {'user_repeat': user_repeat})
        user_id = req.POST.get("stuId", "")
        user_school = req.POST.get("school", "")
        user_email = req.POST.get("email", "")
        user_tel = req.POST.get("tel", "")
        user = User.objects.create_user(username=user_name, password=user_pwd)
        user.school = user_school
        user.stuId = user_id
        user.email = user_email
        user.tel = user_tel
        user.save()
        req.session['is_login'] = True
        req.session['user_id'] = user.id
        req.session['user_name'] = user_name
        auth.login(req, user)
        return HttpResponseRedirect('/index/')
    return render(req, 'register.html')

# 登陆


def login_view(req):
    if req.session.get('is_login', None):
        return HttpResponseRedirect('/index/')
    if req.method == 'POST':
        username = req.POST.get('user_name')
        password = req.POST.get('user_password')
        user = authenticate(username=username, password=password)
        if user:
            auth.login(req, user)
            req.session['is_login'] = True
            req.session['user_id'] = user.id
            req.session['user_name'] = username
            next_url = req.GET.get('next', '')
            if next_url != '':
                return HttpResponseRedirect(next_url)
            return render(req, 'index.html')
        else:
            return render(req, 'login.html', {'user_error': True})
        # if uf.is_valid():                   # 确保用户名和密码都不为空
        #     # 获取表单用户密码
        #
        #     # 获取的表单数据与数据库进行比较
        #     user = authenticate(username=username, password=password)
        #     if user:
        #         # 比较成功，跳转index
        #         auth.login(req, user)
        #         req.session['is_login'] = True
        #         req.session['user_id'] = user.id
        #         req.session['user_name'] = username
        #         next_url = req.GET.get('next', '')
        #         if next_url != '':
        #             return HttpResponseRedirect(next_url)
        #         return render(req, 'index.html')
        #     else:
        #         #比较失败，还在login
        #         message = "username or password wrong!"
        #         return render(req, 'login.html', locals())
        # else:
        #     message = '所有字段都必须填写！'
        #     return render(req, 'login.html', locals())
    # else:
    #     uf = LoginForm(req.POST)
    return render(req, 'login.html', locals())

# 登出


@csrf_exempt
def logout_view(req):
    if not req.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return HttpResponseRedirect("/index/")
    auth.logout(req)
    req.session.flush()
    # 或者使用下面的方法
    # del req.session['is_login']
    # del req.session['user_id']
    # del req.session['user_name']
    return HttpResponseRedirect("/login/")


def user_rank(req):
    return render(req, 'rank.html')

