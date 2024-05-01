from django.urls import path
from langganan.views import *

app_name = 'langganan'

urlpatterns = [
    path('', langganan_paket, name='langganan_paket'),
    path('pembayaran/<str:jenis>/<str:harga>/', pembayaran_paket, name='pembayaran_paket'),
    path('riwayat-transaksi/', riwayat_transaksi, name='riwayat_transaksi'),
]