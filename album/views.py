from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def album_create(request):
    labels = ['Pilih Label', 'Lanskap', 'Potret', 'Alam', 'Seni']  # List data label
    return render(request, 'album_form.html', {'labels': labels})

def album_list(request):
    albums = [
        {'id': 1, 'judul': 'Album 1', 'label': 'Label A', 'jumlah_lagu': 0, 'total_durasi': 0},
        {'id': 2, 'judul': 'Album 2', 'label': 'Label B', 'jumlah_lagu': 2, 'total_durasi': 4},
        {'id': 3, 'judul': 'Album 3', 'label': 'Label C', 'jumlah_lagu': 12, 'total_durasi': 52},
    ]

    user = "Songwriter"
    if user != "Label":
        return render(request, 'album_list.html', {'albums': albums, 'user': user})
    else:
        return render(request, 'album_list_label.html', {'albums': albums, 'user': user})

@csrf_exempt
def tambah_lagu(request, id):
    album = {'id': id, 'judul': 'Album 1', 'label': 'Lanskap', 'jumlah_lagu': 10, 'total_durasi': 45}

    dummy_artists = ['Artist1', 'Artist2', 'Artist3']
    dummy_songwriters = ['Songwriter1', 'Songwriter2', 'Songwriter3']
    dummy_genres = ['Pop', 'Rock', 'Jazz', 'Hip Hop']

    user_logged_in = request.session.get('user_logged_in', None)

    return render(request, 'lagu_add.html', {
        'album': album,
        'user_logged_in': user_logged_in,
        'artists': dummy_artists,
        'songwriters': dummy_songwriters,
        'genres': dummy_genres
    })

def daftar_lagu(request, id):
    lagu_dummy = [
        {'judul': 'Lagu 1', 'durasi': '2', 'total_play': 3, 'total_download': 0},
        {'judul': 'Lagu 2', 'durasi': '3', 'total_play': 2, 'total_download': 2},
        {'judul': 'Lagu 3', 'durasi': '2', 'total_play': 8, 'total_download': 6},
    ]

    album_dummy = {'judul': '1'}

    return render(request, 'lagu_list.html', {'album': album_dummy, 'songs': lagu_dummy})