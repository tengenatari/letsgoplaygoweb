from enum import unique
from types import NoneType

from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class Client(AbstractUser):
    name = models.CharField(blank=True, null=True, default="")
    birthday = models.DateField(blank=True, null=True, default=NoneType)


class Genre(models.Model):
    genre_id = models.AutoField(primary_key=True, null=False, unique=True)

    genre_title = models.CharField(null=False)

    def __str__(self):
        return self.genre_title.__str__()


class Movie(models.Model):
    genre_id = models.AutoField(primary_key=True, null=False, unique=True)

    movie_title = models.CharField(null=False)
    release_date = models.DateField()
    age_limit = models.PositiveIntegerField(null=False)

    genres = models.ManyToManyField(Genre)


class Hall(models.Model):
    hall_id = models.AutoField(primary_key=True, null=False, unique=True)
    hall_title = models.CharField(null=False)


class Row(models.Model):
    row_id = models.AutoField(primary_key=True, null=False, unique=True)

    row_num = models.PositiveIntegerField(null=False)
    num_seats = models.PositiveIntegerField(null=False)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(row_num__gte=1), name="num_row_gte_1" ),
            models.CheckConstraint(check=models.Q(num_seats__gte=1), name="num_seats_gte_1")
        ]

    hall_id = models.ForeignKey(Hall, null=False, on_delete=models.PROTECT)


class Session(models.Model):
    session_id = models.AutoField(primary_key=True, null=False, unique=True)

    start_time = models.DateTimeField()
    cost = models.FloatField(null=False)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(cost__gte=0), name="cost_gte_0" )
        ]

    hall_id = models.ForeignKey(Hall, null=False, on_delete=models.PROTECT)
    movie_id = models.ForeignKey(Movie, null=False, on_delete=models.PROTECT)


class Ticket(models.Model):
    ticket_id = models.AutoField(primary_key=True, null=False, unique=True)

    purchase_time = models.DateTimeField(null=False)
    row = models.PositiveIntegerField(null=False)
    seat = models.PositiveIntegerField(null=False)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(seat__gte=1), name="seat_gte_1"),
            models.CheckConstraint(check=models.Q(row__gte=1), name="row_gte_1")
        ]

    client_id = models.ForeignKey(Client, null=False, on_delete=models.PROTECT)
    session_id = models.ForeignKey(Session, null=False, on_delete=models.PROTECT)

