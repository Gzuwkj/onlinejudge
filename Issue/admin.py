from django.contrib import admin
from .models import Problem


class ProblemAdmin(admin.ModelAdmin):
    list_display = ('no', 'title', 'classification', 'probAuthority', 'probSource')
    list_filter = ('classification', 'probAuthority')
    # fields = ('title', 'content', 'myInput', 'myOutput', 'time', 'memory', 'sampleInput', 'sampleOutput',
    #           'standardInput', 'standardOutput', 'tips', 'probSource', 'classification', 'probAuthority', 'weight')


admin.site.register(Problem, ProblemAdmin)


