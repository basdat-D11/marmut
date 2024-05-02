from django.shortcuts import render

def royalti_list(request):
    list_royalti = [
        {'judul': 'Lagu 1', 'judul_album': 'Album 1', 'total_play': 3, 'total_download': 0, 'jumlah': 450000},
        {'judul': 'Lagu 2', 'judul_album': 'Album 2', 'total_play': 2, 'total_download': 2, 'jumlah': 520000},
        {'judul': 'Lagu 3', 'judul_album': 'Album 3', 'total_play': 1, 'total_download': 0, 'jumlah': 240000},
    ]

    return render(request, 'royalti_list.html', {'list_royalti': list_royalti})