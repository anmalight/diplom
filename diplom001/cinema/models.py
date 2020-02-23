from django.db import models

# Create your models here.

from authentication.models import User


class Movie(models.Model):
    name = models.CharField(max_length=120)
    info = models.CharField(max_length=1000, blank=True, null=True)
    poster = models.ImageField(upload_to='pic_folder/', blank=True, null=True)
    display_date_start = models.DateField()
    display_date_end = models.DateField()

    def __str__(self):
        return self.name


class CinemaHall(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='pic_folder/', blank=True, null=True)
    seats = models.PositiveIntegerField()
    created_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_on = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.name


class MovieSession(models.Model):
    film = models.ForeignKey(Movie, related_name='sessions', on_delete=models.CASCADE)
    hall = models.ForeignKey(CinemaHall, related_name='sessions', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    time_from = models.DateTimeField()
    time_to = models.DateTimeField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    available_seats = models.PositiveIntegerField(blank=True)

    def __str__(self):
        return f"Movie session of film '{self.film.name}' at {self.hall.name} hall"


class Ticket(models.Model):
    session = models.ForeignKey(MovieSession, related_name='tickets', on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, related_name='tickets', on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=1)
    created_on = models.DateTimeField(auto_now_add=True)

    def get_cost(self):
        return self.session.price * self.amount

    def buy(self, price, quantity, session):
        # buy and add to total_bonuses
        self.buyer.bonuses -= price * int(quantity)
        self.buyer.save()
        self.session.available_seats -= int(quantity)
        self.session.save()
        self.buyer.total_bonuses += price * int(quantity)
        self.buyer.save()

    def __str__(self):
        return f"Ticket of film '{self.session.film.name}' at {self.session.time_from}"
