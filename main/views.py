import datetime

from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.template.loader import render_to_string
from .forms import *
from django.core.paginator import Paginator
from .models import *
from asgiref.sync import sync_to_async
from django.db.models import ProtectedError

import os
import main

from fpdf import FPDF, HTMLMixin

pth = os.path.dirname(main.__file__)

models = {"movie": Movie, "genre": Genre, "client": Client, "row": Row, "session": Session, "hall": Hall,
          "ticket": Ticket}
from django.db import connection

cursor = connection.cursor()


class HtmlPdf(FPDF, HTMLMixin):
    pass


def get_pages(instance, page, model, kwargs):
    kwargs = dict(kwargs)
    for x in kwargs.keys():
        kwargs[x] = kwargs[x][0]
    paginator = Paginator(instance.objects.filter(**dict(kwargs)).all(), 10)

    response = {
        "data": paginator.get_page(page),
        "num_left": page - 1,
        "num_page": page,
        "num_right": page + 1,
        "pages": paginator.num_pages,
        "model": model
    }
    return response


def create_form(request, instance, instance_id, model):
    if not (form_name := update(request, model, instance)):
        instance = get_object_or_404(model, **instance_id)
        form_name = Forms(model).form(instance=instance)
    else:
        form_name, instance = form_name
    return form_name, instance


def create(request, model):
    form = Forms(models[model]).form()
    if request.method == 'POST':
        form = Forms(models[model]).form(request.POST)
        if form.is_valid():
            form = form.save()
            return redirect(f'/update/{model}/{form.pk}')
    some = dict()
    some[f"{model}_id"] = 0
    return render(request, f'{model}_update.html', context={'form': form, model: some})

def main(request):
    return redirect('/movie/1')


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

    return render(request, 'raw.html', context={"form": form_model, "URL": f'/raw/{str_model}/add'})


def create_ticket(request, session, row, seat):
    form_ticket = Forms(Ticket).form(initial={'session_id': session, 'row': row, 'seat': seat})
    if request.method == 'POST':
        form_ticket = Forms(Ticket).form(request.POST)
        if form_ticket.is_valid():
            ticket = form_ticket.save()
            return redirect(f'/update/ticket/{ticket.pk}')
    session = get_object_or_404(Session, pk=session)
    return render(request, "create_ticket.html", context={"form": form_ticket, "session": session.__str__(), "seat": seat, "row": row})


def read_model(request, model, page):
    print(request.GET)
    table = models[model]
    response = get_pages(table, page, model, request.GET)
    return render(request, f'{model}.html', context=response)


def update(request, table, instance):
    if request.method == 'POST':
        print(request.POST)
        form = Forms(table).form(request.POST or None, instance=instance)
        print(form.is_valid())
        if form.is_valid():
            form.save()
        else:
            return form, instance


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
        matrix_tickets.append([False]*row.num_seats)

    for ticket in tickets:
        if ticket.row in rows and 1 <= ticket.seat <= rows[rows.index(ticket.row)]:
            matrix_tickets[rows.index(ticket.row)][ticket.seat-1] = ticket

    for i in range(len(rows)):
        matrix_hall.append(list(zip(list(range(1, rows[i]+1)), matrix_tickets[i])))

    matrix_hall = zip(matrix_hall, rows)
    return render(request, 'session_update.html', context={"session": session, "form": form_session,
                                                           "tickets": tickets, "hall": matrix_hall})


def update_ticket(request, ticket_id):

    instance = get_object_or_404(Ticket, ticket_id=ticket_id)

    form_ticket, ticket = create_form(request, instance, {"ticket_id": ticket_id}, Ticket)

    return render(request, 'ticket_update.html', context={"ticket": ticket, "form": form_ticket})


def update_movie(request, movie_id):
    instance = get_object_or_404(Movie, movie_id=movie_id)

    form_movie, movie = create_form(request, instance, {"movie_id": movie_id}, Movie)

    sessions = Session.objects.filter(movie_id=movie_id).all()

    return render(request, 'movie_update.html', context={"movie": movie, "sessions": sessions, "form": form_movie})


def update_hall(request, hall_id):

    instance = get_object_or_404(Hall, hall_id=hall_id)

    form_hall, hall = create_form(request, instance, {'hall_id': hall_id}, Hall)

    rows = Row.objects.filter(hall_id=hall_id).all()

    return render(request, 'hall_update.html', context={"hall": hall, "form": form_hall, "rows": rows})


def update_row(request, row_id):
    instance = get_object_or_404(Row, row_id=row_id)

    form_row, row = create_form(request, instance, {"row_id": row_id}, Row)

    return render(request, 'row_update.html', context={"row": row, "form": form_row})


def update_client(request, client_id):
    instance = get_object_or_404(Client, client_id=client_id)

    form_client, client = create_form(request, instance, {"client_id": client_id}, Client)

    data = Ticket.objects.filter(client_id=client_id)

    return render(request, 'client_update.html', context={"client": client, "form": form_client, "data": data})


def delete_model(request):
    if request.method == 'POST':
        table_id = request.POST['id']
        table = models[request.POST['table']]
        print(table, table_id)
        try:
            table.objects.filter(pk=table_id).delete()

        except ProtectedError:
            return render(request, f'{request.POST['table']}_error_protected.html')
    return redirect('/')


async def first_otchet(request):
    cursor.execute('''SELECT DISTINCT
main_movie.movie_id,
main_movie.movie_title
FROM main_movie INNER JOIN main_movie_genres ON
	main_movie.movie_id = main_movie_genres.movie_id
	AND main_movie_genres.genre_id IN
		(SELECT 
		 main_genre.genre_id
		FROM main_genre INNER JOIN main_movie_genres ON
			main_genre.genre_id = main_movie_genres.genre_id
			INNER JOIN main_movie ON
			main_movie_genres.movie_id = main_movie.movie_id
			INNER JOIN main_session ON
			main_session.movie_id_id = main_movie.movie_id
			INNER JOIN main_ticket ON
			main_ticket.session_id_id = main_session.session_id
		GROUP BY
			main_genre.genre_id,
			main_genre.genre_title
		ORDER BY 
			COUNT(main_ticket.ticket_id) DESC
		LIMIT 3)''')

    rows = cursor.fetchall()

    pdf = HtmlPdf()
    pdf.add_page()
    string = render_to_string('pdf\\some_template.html', context={'table': rows, "titles": ["Номер фильма", "Название фильма"], "main_title": "Отчет о самых популярных фильмах"})
    pdf.add_font('DejaVu', '', 'main\\static\\fonts\\DejaVuSansCondensed.ttf', uni=True)
    pdf.add_font('DejaVu', 'B', 'main\\static\\fonts\\DejaVuSansCondensed-Bold.ttf', uni=True)
    pdf.set_font('DejaVu', '', 14)
    pdf.write_html(string)
    pdf.output(f"main\\static\\reports\\first_{hash(datetime.datetime.now())}.pdf")
    return redirect("/")


async def second_otchet(request):
    cursor.execute('''SELECT 
main_movie.movie_title, 
COALESCE(ticket_count, 0) AS total_tickets 
	FROM main_movie LEFT JOIN main_session ON
	main_movie.movie_id = main_session.movie_id_id 
	LEFT JOIN (
		SELECT 
			main_ticket.session_id_id, 
			COUNT(*) AS ticket_count
		FROM main_ticket 
		GROUP BY main_ticket.session_id_id
	) AS ticket_summary ON
	main_session.session_id = ticket_summary.session_id_id
ORDER BY
	total_tickets DESC
''')

    rows = cursor.fetchall()

    pdf = HtmlPdf()
    pdf.add_page()
    string = render_to_string('pdf\\some_template.html', context={'table': rows, "titles": ["Название фильма", "Количество проданных билетов"], "main_title": "Продажа билетов"})
    pdf.add_font('DejaVu', '', 'main\\static\\fonts\\DejaVuSansCondensed.ttf', uni=True)
    pdf.add_font('DejaVu', 'B', 'main\\static\\fonts\\DejaVuSansCondensed-Bold.ttf', uni=True)
    pdf.set_font('DejaVu', '', 14)
    pdf.write_html(string)
    pdf.output(f"main\\static\\reports\\second-{hash(datetime.datetime.now())}.pdf")
    return redirect("/")


async def third_otchet(request):
    await sync_to_async(cursor.execute)('''SELECT
                    main_session.session_id,
                    movie_title,
                    hall_title,
                    start_time,
     SUM(num_seats),
     (SELECT COUNT(ticket_id) FROM main_ticket WHERE main_ticket.session_id_id = main_session.session_id),
                    SUM(num_seats) - (SELECT COUNT(ticket_id) FROM main_ticket WHERE main_ticket.session_id_id = main_session.session_id) 
                    FROM main_session
                    INNER JOIN main_movie ON
                    main_session.movie_id_id = main_movie.movie_id
                    INNER JOIN main_hall ON
                    main_session.hall_id_id = main_hall.hall_id
                    INNER JOIN main_row ON
                    main_hall.hall_id = main_row.hall_id_id
                    GROUP BY
                    main_session.session_id,
                    movie_title,
                    hall_title,
                    start_time,
                    duration_time
                    LIMIT 30''')
    rows = cursor.fetchall()

    pdf = HtmlPdf()
    pdf.add_page()
    string = await sync_to_async(render_to_string)('pdf\\some_template.html',
                              context={'table': rows, "titles": ["Сеанс", "Название фильма", "Зал", "Дата проведения", "Количество мест всего", "Количество занятых мест", "Количество свободных мест"], "main_title": "Отчет о свободных местах"})
    pdf.add_font('DejaVu', '', 'main\\static\\fonts\\DejaVuSansCondensed.ttf', uni=True)
    pdf.add_font('DejaVu', 'B', 'main\\static\\fonts\\DejaVuSansCondensed-Bold.ttf', uni=True)
    pdf.set_font('DejaVu', '', 10)
    await sync_to_async(pdf.write_html)(string)
    pdf.output(f"main\\static\\reports\\third-{hash(datetime.datetime.now())}.pdf")
    return redirect("/")
