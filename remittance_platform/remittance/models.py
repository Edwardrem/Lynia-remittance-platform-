from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group, Permission


class User(AbstractUser):
    phone_number = models.CharField(max_length=10)
    groups = models.ManyToManyField(Group, through='User_groups', related_name='users')
    user_permissions = models.ManyToManyField(Permission, through='User_user_permissions', related_name='users')


class Transaction(models.Model):
    sender = models.CharField(max_length=255)
    recipient = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)
    status = models.CharField(max_length=20)
    transaction_status = models.CharField(max_length=255, blank=True, null=True)


class TransactionHistory(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='transaction_histories')
    timestamp = models.DateTimeField(auto_now_add=True)


class LogEntry(models.Model):
    action_time = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='log_entries')
    content_type = models.ForeignKey('contenttypes.ContentType', on_delete=models.CASCADE, blank=True, null=True, related_name='log_entries')
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField(blank=True)


class ContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        unique_together = (('app_label', 'model'),)

    def __str__(self):
        return self.model


class User_groups(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    class Meta:
        db_table = 'remittance_user_groups'


class User_user_permissions(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

    class Meta:
        db_table = 'remittance_user_user_permissions'