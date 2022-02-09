from django.contrib import admin
from users.models import ZetUser


@admin.register(ZetUser)
class ZetUserAdmin(admin.ModelAdmin):
    search_fields = ('username',)
    ordering = ('username',)

    class Meta:
        model = ZetUser
        verbose_name = 'user'
        verbose_name_plural = 'users'
