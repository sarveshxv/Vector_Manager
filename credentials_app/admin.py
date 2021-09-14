from django.contrib import admin
from .models import Account
# Register your models here.


class AccountAdmin(admin.ModelAdmin):
    # list_display = ('user', 'platform', 'username')
    list_display = ('platform', 'username')


admin.site.register(Account, AccountAdmin)
