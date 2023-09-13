from django.db import models
from django.contrib.auth.models import AbstractUser


class User(models.Model):
    username = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=10)

class RemittanceUser(AbstractUser):
    new_password1 = models.CharField(max_length=128, verbose_name='password',
                                   help_text='<ul><li>Your password must be at least 8 characters long.</li>'
                                               '<li>Your password must contain at least one uppercase letter.</li>'
                                               '<li>Your password must contain at least one lowercase letter.</li>'
                                               '<li>Your password must contain at least one number.</li>'
                                               '<li>Your password must contain at least one special character.</li></ul>')
    new_password2 = models.CharField(max_length=128, verbose_name='password confirmation',
                                   help_text='Enter the same password as above, for verification.')



    


class Transaction(models.Model):
    sender = models.CharField(max_length=255)
    recipient = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)
    status = models.CharField(max_length=20)


class TransactionHistory(models.Model):
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='transactionhistory_senders',
    )
    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='transactionhistory_recipients',
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)
    status = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

