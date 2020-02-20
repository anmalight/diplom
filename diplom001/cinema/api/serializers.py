from rest_framework import serializers
from cinema.models import MovieSession, Movie, CinemaHall
from authentication.models import User


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'


class MovieSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieSession
        fields = ['film', 'hall', 'price', 'time_from', 'time_to', 'available_seats']


class CinemaHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = CinemaHall
        fields = '__all__'


# ---------------


class GoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieSession
        fields = ['film', 'hall', 'price', 'time_from', 'time_to', 'available_seats']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'



