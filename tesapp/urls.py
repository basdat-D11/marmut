from django.urls import path
from tesapp.views import *


app_name = 'tesapp'

urlpatterns = [
    path('', show_akun, name='show_akun'),
    path('show_konten', show_konten, name='show_konten')
]