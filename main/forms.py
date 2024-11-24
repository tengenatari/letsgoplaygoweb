from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from .models import *

class UserForm(UserCreationForm):
    email = forms.EmailField(required=False)

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def confirm_login_allowed(self, user):
        pass

    class Meta:
        model = User
        fields = ('username', 'password')


class CreateTable(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CreateTable, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}


class MovieForm(CreateTable):
    class Meta:
        fields = "__all__"
        model = Movie


class Forms:
    def __init__(self, table, *args, **kwargs):
        class TableForm(CreateTable):
            class Meta:
                fields = "__all__"
                model = table
        self.form = TableForm
