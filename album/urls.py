from django.urls import path
from album.views import *

app_name = 'album'

urlpatterns = [
    path('', album_list, name='album_list'),
    path('create', album_create, name='album_create'),
    path('<int:id>/add-song', tambah_lagu, name='tambah_lagu'),
    path('<int:id>/list-song', daftar_lagu, name='daftar_lagu'),
]