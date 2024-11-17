from django.shortcuts import render
from django.contrib.auth import base_user
from .forms import UserForm


def main(request):
    return render(request, 'base.html')


def auth(request):
    return render(request, 'auth.html', context={"form": UserForm})
