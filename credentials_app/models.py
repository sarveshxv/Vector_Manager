from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Account(models.Model):
    belongs_to = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    platform = models.CharField(max_length=30)
    platform_slug = models.CharField(max_length=30)
    username = models.CharField(max_length=25, blank=True, null=True)
    password = models.CharField(max_length=30)
    email = models.EmailField(blank=True, null=True)
    mobile = models.IntegerField(blank=True, null=True)
    update = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('modify_account', args=[self.id])

    @staticmethod
    def get_all_accounts():
        return Account.objects.all()

    @staticmethod
    def get_user_accounts(user):
        accounts = Account.get_all_accounts()
        acts = [account for account in accounts if account.belongs_to == user]
        return acts
