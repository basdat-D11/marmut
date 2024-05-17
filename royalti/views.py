from django.shortcuts import redirect, render

from utils.query import query

def royalti_list(request):
    if not 'akun' in request.session:
        return redirect('main:page_login')
    akun = request.session.get('akun', None)
    print(akun)
    role = akun.get('role', 'label')

    if role == 'artis':
        role = 'artist'

    text_email = 'email' if role == 'label' else 'email_akun'

    query_str = f"""SELECT r.id_song, s.total_play, p.rate_royalti
    FROM royalti r, song s, pemilik_hak_cipta p
    WHERE r.id_song = s.id_konten AND
        p.id = r.id_pemilik_hak_cipta
    """
    result = query(query_str)
    for r in result:
        query_str = f"""
        UPDATE royalti
        SET jumlah = {r['total_play'] * r['rate_royalti']}
        WHERE id_song = '{r['id_song']}'
        """
        query(query_str)


    # pre_cond = query(query_str)

    query_str = f"""SELECT id_pemilik_hak_cipta
    FROM {role}
    WHERE {text_email} = '{akun['email']}'
    """
    print(query_str)
    id_pemilik_hak_cipta = query(query_str)[0]['id_pemilik_hak_cipta']
    print(id_pemilik_hak_cipta)
    # k.judul, a.judul, s.total_play, s.total_download, r.jumlah
    query_str = f"""SELECT k.judul, s.total_play, s.total_download, r.jumlah
    FROM konten as k, album as a, song as s, royalti as r
    WHERE r.id_pemilik_hak_cipta = '{id_pemilik_hak_cipta}' AND r.id_song = s.id_konten AND s.id_konten = k.id
     AND a.id = s.id_album
    """

    list_royalti = query(query_str)
    print(list_royalti)

    return render(request, 'royalti_list.html', {'list_royalti': list_royalti})
    