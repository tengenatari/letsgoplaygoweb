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
            user = user_form.save(commit=True)

            return redirect('/login')
        else:
            return render(request, 'auth.html', {'form': user_form})
    return render(request, 'auth.html', context={"form": UserForm})


def login(request):
    if request.method == 'POST':

        loginform = LoginForm(request.POST)
        print(loginform.is_valid())
        print(loginform.__dict__)
        if loginform.is_valid():
            print('a')
            username = loginform.cleaned_data['username']
            password = loginform.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            print(user)
            if user is not None:
                login(request, user)
                return redirect('/')
        return render(request, 'login.html', context={"form": loginform})

    return render(request, 'login.html', context={"form": LoginForm})
