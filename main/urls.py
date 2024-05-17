from django.urls import path
from main.views import *

app_name = 'main'

urlpatterns = [
    path('/tes', home, name='home'),
    path('page_login', page_login, name='page_login'),
    path('handlelogin', login, name='handlelogin'),
    path('dashboard', to_dashboard, name='dashboard'),
    path('validate_login' , validate_login, name='validate_login'),
    path('register_user', register_user, name='register_user'),
    path('register_label', register_label, name='register_label'),
    path('register', register, name='register'),
    path('registrasi_pengguna' , registrasi_pengguna, name='registrasi_pengguna'),
]