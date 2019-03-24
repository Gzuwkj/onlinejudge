from .models import Problem
from django import forms
from django.forms import ModelForm
from django import forms
from django.utils.html import format_html
from django.forms.utils import flatatt
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe


class ProblemForm (ModelForm):
    class Meta:
        model = Problem

        fields = '__all__'

        error_messages = {
            'title': {'required': "标题不能为空", },
            'content': {'required': "内容不能为空", },
        }

        labels = {
            'title': '标题',
            'content': '内容',
            'myInput': '输入',
            'myOutput': '输出',
            'sampleInput': '样列输入',
            'sampleOutput': '样列输出',
            'standardInPut': '标准输入',
            'standardOutPut': '标准输出',
            'tips': '提示',
            'probSource': '题目来源',
            'classification': '分类',
            'probFlag': '判题标记',
            'probAuthority': '权限是否公开',
            'weight': '分数'
        }
