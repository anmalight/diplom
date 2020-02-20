from django.contrib import admin
from cinema.models import MovieSession, Movie, CinemaHall, Ticket
# Register your models here.

admin.site.register(MovieSession)
admin.site.register(Movie)
admin.site.register(CinemaHall)
admin.site.register(Ticket)
