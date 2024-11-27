from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import *
from django.http import HttpResponse
from django.core.paginator import Paginator
from .models import *

models = {"movie": Movie, "genre": Genre, "client": Client, "row": Row, "session": Session, "hall": Hall}


def update(request, table, instance):
    if request.method == 'POST':
        form = Forms(table).form(request.POST or None, instance=instance)
        if form.is_valid():
            form.save()


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
    model = models[str_model]
    form_model = Forms(model).form()
    if request.method == "POST":
        print(str_model)
        form_model = Forms(model).form(data=request.POST)
        if form_model.is_valid():
            print(str_model)
            form_model.save(commit=True)
            return render(request, 'success.html')

    return render(request, 'raw.html', context={"form": form_model, "URL": f'/raw/{str_model}/add'})


def delete_model(request):
    if request.method == 'POST':
        table_id = request.POST['id']
        table = models[request.POST['table']]
        print(table, table_id)
        table.objects.filter(pk=table_id).delete()

        return redirect('/')


def update_movie(request, movie_id):
    instance = get_object_or_404(Movie, movie_id=movie_id)

    update(request, Movie, instance)

    movie = get_object_or_404(Movie, movie_id=movie_id)
    sessions = Session.objects.filter(movie_id=movie_id).all()

    form_movie = Forms(Movie).form(instance=movie)

    return render(request, 'movie_update.html', context={"movie": movie, "sessions": sessions, "form": form_movie})


def update_session(request, session_id):
    instance = get_object_or_404(Session, session_id=session_id)

    update(request, Session, instance)

    session = get_object_or_404(Session, session_id=session_id)
    form_session = Forms(Session).form(instance=session)

    tickets = Ticket.objects.filter(session_id=session_id).all()
    hall = Row.objects.order_by("row_num").filter(hall_id=instance.hall_id)
    matrix_hall = []
    rows = []
    matrix_tickets = []
    for row in hall:
        rows.append(row.num_seats)
        matrix_tickets.append([True]*row.num_seats)

    for ticket in tickets:
        if ticket.row in rows and 1 <= ticket.seats <= rows[rows.index(ticket.row)]:
            matrix_tickets[rows.index(ticket.row)][ticket.seats-1] = False

    for i in range(len(rows)):
        matrix_hall.append(list(zip(list(range(1, rows[i]+1)), matrix_tickets[i])))

    matrix_hall = zip(matrix_hall, rows)
    return render(request, 'session_update.html', context={"session": session, "form": form_session, "tickets": tickets, "hall": matrix_hall})
