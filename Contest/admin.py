from django.contrib import admin
from Contest.models import MatchList


class MatchAdmin(admin.ModelAdmin):
    list_display = ('matchName', 'attribute', 'startTime')
    list_filter = ('attribute', 'startTime')


admin.site.site_header = 'Code Dream 管理平台'
admin.site.site_title = 'Online Judge'

admin.site.register(MatchList, MatchAdmin)
