import datetime

import pytz
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.migrations import serializer
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone  #
from django.views.generic import ListView, CreateView, UpdateView, View
from django.core.exceptions import PermissionDenied, FieldError
from rest_framework import viewsets, permissions, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from authentication.models import User
from cinema.forms import AddMovieSessionForm, AmountForm, AddMovieForm, AddHallForm
from cinema.models import MovieSession, Movie, CinemaHall, Ticket
# Create your views here.
from cinema.api.serializers import GoodSerializer, UserSerializer, MovieSerializer, MovieSessionSerializer, \
    CinemaHallSerializer, TicketSerializer
from datetime import datetime


# api_views start


class MovieViewApi(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]

    def destroy(self,  request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CinemaHallViewApi(viewsets.ModelViewSet):
    queryset = CinemaHall.objects.all()
    serializer_class = CinemaHallSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]

    def update(self, request, *args, **kwargs):
        hall = request.POST.get('hall')
        movie = MovieSession.objects.get(pk=kwargs.get('pk'))
        print(movie)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if len(movie.tickets.all()) >= 1:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MovieSessionViewApi(viewsets.ModelViewSet):
    queryset = MovieSession.objects.all()
    serializer_class = MovieSessionSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]

    def destroy(self,  request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TicketSerializerViewApi(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def destroy(self,  request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def perform_create(self, serializer):
    #     print(self.request.user)
    #     # print(666)
    #
    # def perform_update(self, serializer):
    #     print(self.request.user)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# api_views end


class MovieCreateView(CreateView, LoginRequiredMixin):
    form_class = AddMovieForm
    http_method_names = ['get', 'post']
    template_name = 'cinema/movie_create.html'
    login_url = 'authentication/login/'
    success_url = '/'

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().get(request, *args, **kwargs)
        else:
            raise PermissionDenied()


class HallCreateView(CreateView, LoginRequiredMixin):
    form_class = AddHallForm
    http_method_names = ['get', 'post']
    template_name = 'cinema/hall_create.html'
    login_url = 'authentication/login/'
    success_url = '/'

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().get(request, *args, **kwargs)
        else:
            raise PermissionDenied()


class SessionCreateView(CreateView, LoginRequiredMixin):
    form_class = AddMovieSessionForm
    http_method_names = ['get', 'post']
    template_name = 'cinema/session_create.html'
    login_url = 'authentication/login/'
    success_url = '/'

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().get(request, *args, **kwargs)
        else:
            raise PermissionDenied()

    def post(self, request, *args, **kwargs):
        local = pytz.timezone('Europe/Kiev')
        film = Movie.objects.get(id=int(request.POST.get('film')))
        hall = request.POST.get('hall')
        hall_sessions = MovieSession.objects.filter(hall__id=int(hall))
        start_from_form = (request.POST.get('time_from'))
        end_from_form = (request.POST.get('time_to'))

        if end_from_form < start_from_form:
            messages.error(self.request, "Session could not end before start")
            return HttpResponseRedirect(reverse('add_session'))

        start_new_session = local.localize(datetime.strptime(str(start_from_form), '%m/%d/%Y %H:%M:%S'))
        end_new_session = local.localize(datetime.strptime(str(end_from_form), '%m/%d/%Y %H:%M:%S'))

        for h in hall_sessions:
            start = local.localize(
                datetime.strptime(str(h.time_from), '%Y-%m-%d %H:%M:%S'))  # .start_at), '%Y-%m-%d %H:%M:%S'))
            end = local.localize(datetime.strptime(str(h.time_to), '%Y-%m-%d %H:%M:%S'))

            if (start_new_session.date() > film.display_date_start) and (
                    end_new_session.date() < film.display_date_end):
                if ((start_new_session < start) and (start_new_session < end)) or (
                        (end_new_session > start) and (end_new_session > end)):
                    return super().post(request, *args, **kwargs)
                    # return HttpResponse('N 1')
                else:
                    messages.error(self.request,
                                   'Session could not be created because on not relevant date or time')
                    return HttpResponseRedirect(reverse('session-list'))
        messages.error(self.request, 'Session could not be created because session and movie dates do not match')
        return HttpResponseRedirect(reverse('session-list'))


class MoviesListView(ListView):
    model = Movie
    context_object_name = 'movies'
    template_name = 'cinema/movie_list.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().get(request, *args, **kwargs)
        else:
            raise PermissionDenied()


class CinemaHallListView(ListView):
    model = CinemaHall
    context_object_name = 'cinema_halls'
    template_name = 'cinema/cinema_halls_list.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().get(request, *args, **kwargs)
        else:
            raise PermissionDenied()


class MovieSessionsListView(ListView):
    """ main page. all sessions that are elder then current time"""
    model = MovieSession
    context_object_name = 'sessions'
    template_name = 'cinema/session_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        now = timezone.now()
        today = MovieSession.objects.filter(time_from__gte=now)
        sort = self.request.GET.getlist('sort')
        if sort:
            today = today.order_by(*sort)
        context.update({'amount': AmountForm,
                        'sessions': today})
        return context


class MovieSessionsListViewToday(MovieSessionsListView):
    """ Only sessions for current 24 hours"""

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        now = timezone.now()
        next_day = now + timezone.timedelta(days=1)

        today = MovieSession.objects.filter(time_from__gte=now).filter(time_from__lte=next_day).order_by('time_from')
        context.update({'amount': AmountForm,
                        'sessions': today})
        return context


class MovieSessionsListViewTomorrow(MovieSessionsListView):
    """ Only sessions for the next 24 hours after today"""

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        now = timezone.now() + timezone.timedelta(days=1)
        next_day = now + timezone.timedelta(days=1)

        today = MovieSession.objects.filter(time_from__gte=now).filter(time_from__lte=next_day).order_by('time_from')
        context.update({'amount': AmountForm,
                        'sessions': today})
        return context


class FilmSessionsUpdateView(UpdateView, LoginRequiredMixin):
    template_name = 'cinema/session_update.html'
    form_class = AddMovieSessionForm
    success_url = '/'
    model = MovieSession
    queryset = MovieSession.objects.all()

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().get(request, *args, **kwargs)
        else:
            raise PermissionDenied()

    def post(self, request, *args, **kwargs):
        local = pytz.timezone('Europe/Kiev')
        film = Movie.objects.get(id=int(request.POST.get('film')))
        hall = request.POST.get('hall')
        hall_sessions = MovieSession.objects.filter(hall__id=hall)
        start_from_form = (request.POST.get('time_from'))
        end_from_form = (request.POST.get('time_to'))
        movie = MovieSession.objects.get(pk=kwargs.get('pk'))

        if len(movie.tickets.all()) >=1:
            messages.error(self.request, "Tickets were already sold")
            return HttpResponseRedirect(reverse('session-list'))

        if end_from_form < start_from_form:
            messages.error(self.request, "Session could not end before start")
            return HttpResponseRedirect(reverse('add_session'))

        start_new_session = local.localize(datetime.strptime(str(start_from_form), '%m/%d/%Y %H:%M:%S'))
        end_new_session = local.localize(datetime.strptime(str(end_from_form), '%m/%d/%Y %H:%M:%S'))
        # if MovieSession.objects.all() and (MovieSession.objects.filter(hall_id=hall)):
        for h in hall_sessions:
            start = local.localize(
                datetime.strptime(str(h.time_from), '%Y-%m-%d %H:%M:%S'))
            end = local.localize(datetime.strptime(str(h.time_to), '%Y-%m-%d %H:%M:%S'))

            if (start_new_session.date() > film.display_date_start) and (
                    end_new_session.date() < film.display_date_end):
                if ((start_new_session < start) and (start_new_session < end)) or (
                        (end_new_session > start) and (end_new_session > end)):
                    return super().post(request, *args, **kwargs)
                    # return HttpResponse('N 1')

                messages.error(self.request,
                               'Session could not be updated because on not relevant date or time')
                print(7)
                return HttpResponseRedirect(reverse('session-list'))
        messages.error(self.request, 'Session could not be updated because session and movie dates do not match')
        return HttpResponseRedirect(reverse('session-list'))


class BuyTicketView(CreateView, LoginRequiredMixin):
    template_name = 'cinema/buy_ticket.html'
    # model = Ticket
    http_method_names = ['get', 'post']
    login_url = 'authentication/login/'
    success_url = '/'
    form_class = AmountForm
    session = None

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            raise PermissionDenied()
        else:
            return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.user.is_superuser:
            raise PermissionDenied()
        else:
            self.session = MovieSession.objects.get(id=kwargs.get("session_id"))
            return super().post(request, *args, **kwargs)

    # !!!!!!!!!!!!!!!!!!!!!!!!!!
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.buyer = self.request.user
        obj.session = self.session
        obj.summ = int(self.request.POST.get('amount')) * obj.session.price
        if obj.buyer.bonuses < obj.summ:
            messages.error(self.request, "Sorry. Not enough bonuses")
            return HttpResponseRedirect(reverse('session-list'))
        if obj.session.hall.seats < int(self.request.POST.get('amount')):
            messages.error(self.request, "tickets are not enough in stock")
            return HttpResponseRedirect(reverse('session-list'))
        obj.buy(price=self.session.price, quantity=self.request.POST.get('amount'), session=self.session)
        obj.save()
        return HttpResponseRedirect(self.success_url)


class BuyingList(ListView, LoginRequiredMixin):
    model = Ticket
    # context_object_name = 'tickets'
    template_name = 'cinema/tickets_bonuses.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            raise PermissionDenied()
        else:
            return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs = super(BuyingList, self).get_context_data(**kwargs)
        kwargs.update({
            'tickets': Ticket.objects.filter(buyer_id=self.request.user.id),
            'user_info': User.objects.filter(id=self.request.user.id),
            # 'total_bonuses': Ticket.objects.filter(buyer_id=self.request.user.id).filter(),
            # 'taskd_list': TaskD.objects.all(), tt.objects.aggregate(total_likes=Sum('tt_like'))
        })
        return kwargs
