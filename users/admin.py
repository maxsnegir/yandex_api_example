from users.models import AdvUser
from django.contrib import admin


@admin.register(AdvUser)
class AdvUserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'email',)
