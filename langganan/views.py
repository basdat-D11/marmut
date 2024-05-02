from django.shortcuts import render

# Create your views here.
def langganan_paket(request):
    # Contoh data paket langganan
    paket = [
        {'jenis': '1 Bulan', 'harga': 'Rp50.000'},
        {'jenis': '3 Bulan', 'harga': 'Rp120.000'},
        {'jenis': '6 Bulan', 'harga': 'Rp220.000'},
        {'jenis': '1 Tahun', 'harga': 'Rp400.000'}
    ]
    return render(request, 'langganan_paket.html', {'paket': paket})

def pembayaran_paket(request, jenis, harga):
    # You can add additional logic here if needed
    context = {
        'jenis': jenis,
        'harga': harga,
    }
    return render(request, 'pembayaran_paket.html', context)

def riwayat_transaksi(request):
    # Example static data for transaction history
    transaksi = [
        {
            'jenis': '1 Bulan',
            'tanggal_dimulai': '8 April 2024, 23:00',
            'tanggal_berakhir': '8 Mei 2024, 23:00',
            'metode_pembayaran': 'E-Wallet',
            'nominal': 'Rp50.000'
        }
        # You can add more transactions here
    ]
    return render(request, 'riwayat_transaksi.html', {'transaksi': transaksi})