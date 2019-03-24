from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'tel', 'email', 'school', 'major')
    list_filter = ('school', 'major', 'is_active')


admin.site.register(User, UserAdmin)
