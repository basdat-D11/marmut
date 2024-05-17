from django.urls import path
from .views import kelola_podcast, create_podcast, list_podcast, create_episode, daftar_episode, delete_podcast, delete_episode, play_podcast

app_name = 'podcast'

urlpatterns = [
    path('show_podcast/', kelola_podcast, name='show_podcast'),
    path('create_podcast/', create_podcast, name='create_podcast'),
    path('list_podcast/', list_podcast, name='list_podcast'),
    path('create_episode/', create_episode, name='create_episode'),
    path('daftar_episode/', daftar_episode, name='daftar_episode'),
    path('delete_podcast/', delete_podcast, name='delete_podcast'),
    path('delete_episode/', delete_episode, name='delete_episode'),
    path('play_podcast/', play_podcast, name='play_podcast'),
]
