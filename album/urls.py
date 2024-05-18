from django.urls import path
from album.views import *

app_name = 'album'

urlpatterns = [
    path('', album_list, name='album_list'),
    path('create', album_create, name='album_create'),
    path('<str:id>/add-song', tambah_lagu, name='tambah_lagu'),
    path('<str:id>/list-song', daftar_lagu, name='daftar_lagu'),
    path('delete/<str:id>', delete_album, name='delete_album'),
    path('delete-song/<str:id>', delete_lagu, name='delete_album')
]