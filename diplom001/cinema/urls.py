from django.urls import path

from cinema.views import MovieSessionsListView, FilmSessionsUpdateView, BuyTicketView, MovieCreateView, HallCreateView, \
    SessionCreateView, MoviesListView, MovieSListView, BuyingList, MovieSessionsListViewTomorrow

urlpatterns = [
    path('', MovieSessionsListView.as_view(), name='session-list'),
    path('tomorrow/', MovieSessionsListViewTomorrow.as_view(), name='session-list-tomorrow'),

    path('add_movie/', MovieCreateView.as_view(), name='add_movie'),
    path('add_hall/', HallCreateView.as_view(), name='add_hall'),
    path('movie_list/', MoviesListView.as_view(), name='movie_list'),
    path('hall_list/', MovieSListView.as_view(), name='hall_list'),
    path('tickets_bonuses_list/', BuyingList.as_view(), name='tickets_bonuses_list'),

    path('add_session/', SessionCreateView.as_view(), name='add_session'),
    path('update_session/<int:id>/', FilmSessionsUpdateView.as_view(), name='update_session'),
    path('buy_ticket/<int:session_id>/', BuyTicketView.as_view(), name='buy_ticket'),

]


