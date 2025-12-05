from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from .models import Payout

User = get_user_model()

admin.site.site_header = 'Администрирование Test-task'
admin.site.site_title = 'Test-task Администрирование'
admin.site.index_title = 'Добро пожаловать в панель управления Test-task'
admin.site.empty_value_display = 'Не задано'

admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    pass


@admin.register(Payout)
class PayoutAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'currency', 'status', 'created_by', 'created_at')
    list_filter = ('status', 'currency', 'created_at', 'created_by')
    search_fields = ('id', 'beneficiary_name', 'beneficiary_account', 'description')
    readonly_fields = ('id', 'created_at', 'updated_at')
    ordering = ('-created_at',)
