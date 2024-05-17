from django.shortcuts import render
from utils.query import query

# View for displaying the search bar
def search_bar(request):
    return render(request, 'search_bar.html')

# View for displaying search results
def search_results(request):
    search = request.GET.get('search', '')
    context = {'search': search}

    if search:
        formatted_search = f'%{search}%'
        search_query = f"""
        SELECT konten.judul AS Title, 'Song' AS ContentType, akun.nama AS CreatorName, song.id_konten AS ItemUUID
        FROM song
        JOIN konten ON song.id_konten = konten.id
        JOIN artist ON song.id_artist = artist.id
        JOIN akun ON artist.email_akun = akun.email
        WHERE konten.judul ILIKE '{formatted_search}'

        UNION

        SELECT konten.judul AS Title, 'Podcast' AS ContentType, akun.nama AS CreatorName, podcast.id_konten AS ItemUUID
        FROM podcast
        JOIN konten ON podcast.id_konten = konten.id
        JOIN podcaster ON podcast.email_podcaster = podcaster.email
        JOIN akun ON podcaster.email = akun.email
        WHERE konten.judul ILIKE '{formatted_search}'

        UNION

        SELECT user_playlist.judul AS Title, 'User Playlist' AS ContentType, akun.nama AS CreatorName, user_playlist.id_user_playlist AS ItemUUID
        FROM user_playlist
        JOIN akun ON user_playlist.email_pembuat = akun.email
        WHERE user_playlist.judul ILIKE '{formatted_search}'

        ORDER BY Title ASC;
        """
        data = query(search_query)

        context['results'] = data

    return render(request, 'search_result.html', context)
