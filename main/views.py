from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .forms import UserForm, LoginForm
from django.http import HttpResponse


def main(request):
    return render(request, 'base.html')


def auth(request):

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():

            user = user_form.save(commit=False)
            user.is_active = True
            user.save()
            return redirect('/login')
        else:
            return render(request, 'auth.html', {'form': user_form})
    return render(request, 'auth.html', context={"form": UserForm})


def login_user(request):
    login_form = LoginForm()
    if request.method == 'POST':

        login_form = LoginForm(data=request.POST)

        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
        return render(request, 'login.html', context={"form": login_form})

    return render(request, 'login.html', context={"form": login_form})
