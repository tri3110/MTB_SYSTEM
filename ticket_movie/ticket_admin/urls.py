from django.urls import path
from .views import CinemaView, MovieView, ScreenView, SeatView, ShowtimeView

urlpatterns = [
    path('cinema/create/', CinemaView.as_view(), name='create_cinema'),
    path('cinema/update/<int:id>/', CinemaView.as_view(), name='update_cinema'),
    path('cinema/delete/<int:id>/', CinemaView.as_view(), name='delete_cinema'),
    path('screen/get/', ScreenView.as_view(), name='get_data_screen'),
    path('screen/seat/get/<int:screen_id>/', SeatView.as_view(), name='get_seat_from_screen'),
    path('screen/create/', ScreenView.as_view(), name='create_screen'),
    path('screen/update/<int:id>/', ScreenView.as_view(), name='update_screen'),
    path('screen/delete/<int:id>/', ScreenView.as_view(), name='delete_screen'),
    path('movie/create/', MovieView.as_view(), name='create_movie'),
    path('movie/update/<int:id>/', MovieView.as_view(), name='update_movie'),
    path('movie/delete/<int:id>/', MovieView.as_view(), name='delete_movie'),
    path('showtime/create/', ShowtimeView.as_view(), name='create_showtime'),
    path('showtime/update/<int:id>/', ShowtimeView.as_view(), name='update_showtime'),
    path('showtime/delete/<int:id>/', ShowtimeView.as_view(), name='delete_showtime'),
]
