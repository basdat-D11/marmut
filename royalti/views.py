from django.shortcuts import redirect, render

from utils.query import query

def royalti_list(request):
    if not 'akun' in request.session:
        return redirect('main:page_login')
    akun = request.session.get('akun', None)

    role = akun.get('role', 'podcaster')
    if role == 'podcaster':
        return redirect('main:dashboard')

    if role == 'artis':
        role = 'artist'

    text_email = 'email' if role == 'label' else 'email_akun'

    query_str = f"""
    UPDATE royalti
    SET jumlah =
        (SELECT total_play FROM song WHERE id_konten = id_song)
        *
        (SELECT rate_royalti FROM pemilik_hak_cipta WHERE id_pemilik_hak_cipta = id)
    """
    precond = query(query_str)
    print(precond)

    inner = f"SELECT id_pemilik_hak_cipta FROM {role} WHERE {text_email} = '{akun['email']}'"
    print("OUTPUT:", query(inner))

    query_str = f"""SELECT k.judul, s.total_play, s.total_download, r.jumlah, a.judul as judul_album
    FROM konten as k, album as a, song as s, royalti as r
    WHERE r.id_pemilik_hak_cipta in (SELECT id_pemilik_hak_cipta FROM {role} WHERE {text_email} = '{akun['email']}')
     AND r.id_song = s.id_konten AND s.id_konten = k.id
     AND a.id = s.id_album
    """

    list_royalti = query(query_str)
    print(list_royalti)

    data = {'list_royalti': list_royalti}
    data.update(akun)

    return render(request, 'royalti_list.html', data)
    