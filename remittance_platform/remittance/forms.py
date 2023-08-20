from django import forms
from remittance.models import Transaction
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.contrib.auth import authenticate

class CreateTransactionForm(forms.Form):
    sender = forms.CharField(max_length=255)
    recipient = forms.CharField(max_length=255)
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    currency = forms.CharField(max_length=3)

class TransactionHistoryForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ['sender', 'recipient', 'amount', 'currency', 'status']

class UpdateTransactionStatusForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ['status']

class LoginForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(max_length=128, widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        user = authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError('Invalid username or password.')

        self.user = user
        return self.cleaned_data
    

class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already exists.')

        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email address already exists.')

        return email

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 != password2:
            raise forms.ValidationError('Passwords do not match.')

        return password2
    
class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(max_length=255)

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email address not found.')

        return email
    
class ResetPasswordForm(forms.Form):
    new_password1 = forms.CharField(max_length=128, widget=forms.PasswordInput)
    new_password2 = forms.CharField(max_length=128, widget=forms.PasswordInput)

    def clean_new_password2(self):
        new_password1 = self.cleaned_data['new_password1']
        new_password2 = self.cleaned_data['new_password2']

        if new_password1 != new_password2:
            raise forms.ValidationError('Passwords do not match.')

        return new_password2

