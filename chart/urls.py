from django.urls import path, include
from . import views

app_name = 'chart'

urlpatterns = [
    path('lihat_chart/', views.lihat_chart, name='lihat_chart'),
    path('detail_chart/', views.detail_chart, name='detail_chart'),
    path('playlist/', include('playlist.urls')),
]
