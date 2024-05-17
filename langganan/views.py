from pyexpat.errors import messages
from django.shortcuts import render, redirect
from utils.query import query
import uuid
from datetime import datetime, timedelta

# Create your views here.
def langganan_paket(request):
    akun = request.session.get('akun', None)

    role = akun['role']
    premium = akun['premium']

    paket = [
        {'jenis': '1 Bulan', 'harga': 'Rp50.000'},
        {'jenis': '3 Bulan', 'harga': 'Rp120.000'},
        {'jenis': '6 Bulan', 'harga': 'Rp220.000'},
        {'jenis': '1 Tahun', 'harga': 'Rp400.000'}
    ]
    return render(request, 'langganan_paket.html', {'paket': paket, 'role': role, 'premium': premium})

def pembayaran_paket(request, jenis, harga):
    akun = request.session.get('akun', None)

    role = akun['role']
    premium = akun['premium']

    if request.method == 'POST':
        email = akun['email']
        metode_bayar = request.POST.get('payment_method')
        nominal = int(harga.replace('Rp', '').replace('.', ''))

        id_transaksi = str(uuid.uuid4())

        timestamp_dimulai = datetime.now()

        if jenis == '1 Bulan':
            duration_months = 1
        elif jenis == '3 Bulan':
            duration_months = 3
        elif jenis == '6 Bulan':
            duration_months = 6
        elif jenis == '1 Tahun':
            duration_months = 12

        timestamp_berakhir = timestamp_dimulai + timedelta(days=30*duration_months)

        query_str = f"""
        INSERT INTO marmut.transaction (id, jenis_paket, email, timestamp_dimulai, timestamp_berakhir, metode_bayar, nominal)
        VALUES ('{id_transaksi}', '{jenis}', '{email}', '{timestamp_dimulai}', '{timestamp_berakhir}', '{metode_bayar}', {nominal});
        """

        query(query_str)

        if akun['premium'] == False:
            akun['premium'] = True
            request.session['akun'] = akun
            return redirect('langganan:riwayat_transaksi')
        else:
            context = {
                'jenis': jenis,
                'harga': harga,
                'error_message': "Pengguna masih memiliki paket aktif. Transaksi dibatalkan."
            }
            return render(request, 'pembayaran_paket.html', context)

    context = {
        'jenis': jenis,
        'harga': harga,
        'role': role,
        'premium': premium
    }
    return render(request, 'pembayaran_paket.html', context)

def riwayat_transaksi(request):
    akun = request.session.get('akun', None)

    role = akun['role']
    premium = akun['premium']

    if akun:
        email = akun['email']
        query_str = f"""
        SELECT t.jenis_paket AS jenis, t.timestamp_dimulai AS tanggal_dimulai, t.timestamp_berakhir AS tanggal_berakhir, t.metode_bayar AS metode_Pembayaran, t.nominal AS nominal
        FROM marmut.transaction t
        JOIN marmut.akun a ON t.email = a.email
        WHERE a.email = '{email}';
        """
        transaksi = query(query_str)
    else:
        transaksi = []

    return render(request, 'riwayat_transaksi.html', {'transaksi': transaksi, 'role': role, 'premium': premium})
