from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import *
from django.http import HttpResponse
from django.core.paginator import Paginator
from .models import *


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


def logout_view(request):
    logout(request)
    return redirect('/')


def save_create_movie(request, page=1):
    paginator = Paginator(Movie.objects.all(), 10)

    if request.method == 'POST':
        if request['type'] == 'delete':
            Movie.objects.filter(pk__in=request.POST['movie']).delete().save()


    response = {
        "data": paginator.get_page(page),
        "num_page": page,
        "pages": paginator.page_range

    }

    return render(request, 'movie.html', context=response)


def create_model(request, str_model):
    print(request.__dict__)
    model = {"movie": Movie, "genre": Genre, "client": Client, "row": Row, "session": Session, "hall": Hall}[str_model]
    form_model = Forms(model).form()
    if request.method == "POST":
        print(str_model)
        form_model = Forms(model).form(data=request.POST)
        if form_model.is_valid():
            print(str_model)
            form_model.save(commit=True)
            return render(request, 'success.html')

    return render(request, 'raw.html', context={"form": form_model, "URL": f'/raw/{str_model}/add'})

