from django import forms
from django.forms import ModelForm
from UserProfile.models import User

from captcha.fields import CaptchaField

class LoginForm(forms.Form):
    username = forms.CharField(max_length=30,label='用户名',widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(max_length=50,label='密码', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField(label='验证码')
    class Meta:
        model = User


class RegisterForm(ModelForm):
    captcha = CaptchaField(label='验证码')
    class Meta:
        model = User
        fields = [
             "username",
             "password",
             "school",
             "major",
             "myClass",
             "stuId",
             "headImage",
             "synopsis",
             "email",
             "tel" ,
        ]

        attrs = {
        	'class': 'form-control'
        }

        error_messages = {
            'username': {'required': "用户名不能为空", },
            'tel': {'required': "手机号码不能为空", },
        }

        labels = {
            'username': '用户名',
            'password': '密码',
            'school': '学校',
            'major': '专业',
            'myClass': '班级',
            'stuId': '学号',
            'headImage': '头像',
            'synopsis': '个人简介',
            'email': '邮箱',
            'tel': '手机号码' ,
        }



class ProfileForm(ModelForm):
    class Meta:
        model = User
        fields = [
             "school",
             "major",
             "myClass",
             "stuId",
             "headImage" ,
             "synopsis",
             "email",
             "tel" ,
        ]

        attrs = {
            'class': 'form-control'
        }

        labels = {
            'school': '学校',
            'major': '专业',
            'myClass': '班级',
            'stuId': '学号',
            'headImage': '头像',
            'synopsis': '个人简介',
            'email': '邮箱',
            'tel': '手机号码' ,
        }


'''
class RegisterForm(ModelForm):
	captcha = CaptchaField(label='验证码')
    class Meta:
        model = User
        fields = [
             "username",
             "password",
             "gender",
             "school",
             "major",
             "myClass",
             "stuId",
             "headImage",
             "synopsis",
             "email",
             "tel" ,
        ]

        attrs = {
        	'class': 'form-control'
        }

        error_messages = {
            'username': {'required': "用户名不能为空", },
            'tel': {'required': "手机号码不能为空", },
        }

        labels = {
            'userName': '用户名',
            'passWord': '密码',
            'gender': '性别',
            'school': '学校',
            'major': '专业',
            'myClass': '班级',
            'stuId': '学号',
            'headImage': '头像',
            'synopsis': '个人简介',
            'email': '邮箱',
            'tel': '手机号码' ,
        }
'''