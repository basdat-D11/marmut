import json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, JsonResponse
from utils.query import query
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from datetime import datetime, timedelta


from uuid import uuid4


def home(request):
    return render(request, 'home.html')


def page_login(request):
    error_message = request.session.pop('error_message', None)
    return render(request, 'login.html', {'error_message': error_message})


@csrf_exempt
def login(request):
    email = request.POST['email']
    password = request.POST['password']
    query_str = f"CALL check_subscription_status('{email}')"
    hasil = query(query_str)
    query_str = f"SELECT * FROM akun WHERE email = '{email}' AND password = '{password}'"
    hasil = query(query_str)
    if len(hasil) == 1:
        """ response = HttpResponseRedirect(reverse("tesapp:show_konten"))
        return response """
        role = []
        #left join dengan artisx
        if cek_artis(email):
            role.append("artis")
        if cek_songwriter(email):
            role.append("songwriter")
        if cek_podcaster(email):
            role.append("podcaster")

        akun = build_akun(email, role)

        akun['nama'] = hasil[0]['nama']
        akun['email'] = hasil[0]['email']
        akun['kota'] = hasil[0]['kota_asal']
        akun['gender'] = hasil[0]['gender']
        akun['tpt_lahir'] = hasil[0]['tempat_lahir']
        #ubah date ke string
        akun['tgl_lahir'] = hasil[0]['tanggal_lahir'].strftime('%Y-%m-%d')
        akun['role'] = role

        query_new = f"SELECT * FROM premium WHERE email = '{email}'"
        prem = query(query_new)

        if len(prem) == 1:
            akun['premium'] = True
        else:
            akun['premium'] = False

    
        query_str = f"SELECT * FROM user_playlist WHERE email_pembuat = '{email}'"
        hasil = query(query_str)
        daftar_playlist = set()
        for playlist in hasil:
            daftar_playlist.add(playlist['judul'])
        daftar_playlist = list(daftar_playlist)
        akun['playlist'] = daftar_playlist

        role_build = ''
        for role in akun['role']:
            role_build += role
            if role != akun['role'][-1]:
                role_build += ', '
        akun['role'] = role_build
        if akun['role'] == '':
            akun['role'] = 'Pengguna Biasa'
        if akun['gender'] == 1:
            akun['gender'] = 'Laki-laki'
        else:
            akun['gender'] = 'Perempuan'
        request.session['akun'] = akun
        request.session.set_expiry(36000)

        return HttpResponseRedirect(reverse('main:dashboard'))

    else:
        query_str = f"SELECT * FROM label WHERE email = '{email}'"
        hasil = query(query_str)
        if len(hasil) == 1:
            akun = {}
            akun['nama'] = hasil[0]['nama']
            akun['email'] = hasil[0]['email']
            akun['kontak'] = hasil[0]['kontak']
            id_label = hasil[0]['id']
            query_str = f"SELECT * FROM album WHERE id_label = '{id_label}'"
            hasil = query(query_str)
            daftar_album = set()
            for album in hasil:
                daftar_album.add(album['judul'])
            daftar_album = list(daftar_album)
            akun['album'] = daftar_album
            request.session['akun'] = akun
            return HttpResponseRedirect('/main/dashboard')
        #request.session['error_message'] = "Email atau password salah. Silakan coba lagi."
        return redirect(reverse('main:page_login'))
    
@csrf_exempt    
def to_dashboard(request):
    akun = request.session.get('akun', None)
    if akun:
        try:
            role = akun['kontak']
            return render(request, 'dasboard_label.html', akun)
        except:
            return render(request, 'dashboard.html', akun)
    else:
        return redirect(reverse('main:page_login'))
    
def cek_artis(email):
    query_str = f"SELECT * FROM artist WHERE email_akun = '{email}'"
    hasil = query(query_str)
    try:
        if len(hasil) == 1:
            return True
        else:
            return False
    except:
        return False
    
def cek_songwriter(email):
    query_str = f"SELECT * FROM songwriter WHERE email_akun = '{email}'"
    hasil = query(query_str)
    try:
        if len(hasil) == 1:
            return True
        else:
            return False
    except:
        return False
    
def cek_podcaster(email):
    query_str = f"SELECT * FROM podcaster WHERE email = '{email}'"
    hasil = query(query_str)
    try:
        if len(hasil) == 1:
            return True
        else:
            return False
    except:
        return False
    
def cek_label(email):
    query_str = f"SELECT * FROM label WHERE email = '{email}'"
    hasil = query(query_str)
    if len(hasil) == 1:
        return True
    else:
        return False
    
def build_akun(email, role):
    akun = {'nama' : '',
            'email' : '',
            'kota' : '',
            'gender' : '',
            'tpt_lahir' : '',
            'tgl_lahir' : '',
            'role' : [],
            'lagu' : [],
            'podcast' : [],
            'playlist' : [],}
    if 'artis' or 'songwriter' in role:
        query_str = f"SELECT * FROM artist WHERE email_akun = '{email}'"
        hasil = query(query_str)
        query_str = f"SELECT * FROM songwriter WHERE email_akun = '{email}'"
        hasil2 = query(query_str)
        id_artis = ''
        id_songwriter = ''
        try:
            id_artis = hasil[0]['id']
        except:
            pass
        try:
            id_songwriter = hasil2[0]['id']
        except:
            pass
        #ambil lagu
        query_str = f"SELECT * FROM song JOIN KONTEN ON id_konten = konten.id AND id_artist = '{id_artis}'"
        hasil = query(query_str)
        daftar_lagu = set()
        try:
            for lagu in hasil:
                daftar_lagu.add(lagu['judul'])
        except:
            pass
        query_str = f"""SELECT * FROM songwriter_write_song
                        JOIN SONG ON songwriter_write_song.id_song = song.id_konten
                        JOIN KONTEN ON song.id_konten = konten.id
                        WHERE songwriter_write_song.id_songwriter = '{id_songwriter}'"""
        hasil = query(query_str)
        try:
            for lagu in hasil:
                daftar_lagu.add(lagu['judul'])
        except:
            pass
        daftar_lagu = list(daftar_lagu)
        akun['lagu'] = daftar_lagu
    if 'podcaster' in role:
        query_str = f"SELECT * FROM podcaster WHERE email = '{email}'"
        hasil = query(query_str)
        email_pod = hasil[0]['email']
        query_str = f"SELECT * FROM podcast JOIN konten ON podcast.id_konten = konten.id AND email_podcaster = '{email_pod}'"
        hasil = query(query_str)
        daftar_podcast = set()
        try:
            for podcast in hasil:
                daftar_podcast.add(podcast['judul'])
        except:
            pass
        daftar_podcast = list(daftar_podcast)
        akun['podcast'] = daftar_podcast
    return akun


def ceklogin(email, password):
    query_str = f"SELECT * FROM akun WHERE email = '{email}' and password = '{password}'"
    hasil = query(query_str)

    try:
        if len(hasil) == 1:
            return True
    except:
        pass
    query_str = f"SELECT * FROM label WHERE email = '{email}' and password = '{password}'"
    hasil = query(query_str)
    try:
        if len(hasil) == 1:
            return True
    except:
        pass
    return False


@csrf_exempt
def validate_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        
        if ceklogin(email, password):
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'message': 'Email atau password salah.'})

def register_user(request):
    return render(request, 'registrasi_pengguna.html')


def register_label(request):
    return render(request, 'registrasi_label.html')

def register(request):
    return render(request, 'register.html')

@csrf_exempt
def registrasi_pengguna(request):
    nama = request.POST.get('nama')
    email = request.POST.get('email')
    password = request.POST.get('password')
    gender = request.POST.get('gender')
    if gender == 'laki-laki':
       gender = 1
    else:
       gender = 0
    kota = request.POST.get('kota-asal')
    tpt_lahir = request.POST.get('tempat-lahir')
    tgl_lahir = request.POST.get('tanggal-lahir')
    role = request.POST.getlist('role')
    if len(role) == 0:
        is_verified = False
    else:
        is_verified = True

    query_str = f"INSERT INTO akun VALUES ('{email}', '{password}', '{nama}', '{gender}', '{tpt_lahir}', '{tgl_lahir}', '{is_verified}', '{kota}')"
    hasil = query(query_str)
    
    if isinstance(hasil, int):
        pass
    else:
        return render(request, 'registrasi_pengguna.html', {'error_message': 'Email sudah terdaftar.'})

    if 'podcaster' in role:
        query_str = f"INSERT INTO podcaster VALUES ('{email}')"
        query(query_str)
    

    id_sw = uuid4()
    id_phc = uuid4()
    id_artis = uuid4()
    if 'songwriter' in role or 'artis' in role:
        query_str = f"INSERT INTO pemilik_hak_cipta VALUES ('{id_phc}', {int('3000')})"
        hasil = query(query_str)
    if 'songwriter' in role:
        query_str = f"INSERT INTO songwriter VALUES ('{id_sw}','{email}', '{id_phc}')"
        hasil = query(query_str)
    if 'artis' in role:
        query_str = f"INSERT INTO artist VALUES ('{id_artis}', '{email}', '{id_phc}')"
        hasil = query(query_str)

    return HttpResponseRedirect(reverse('main:page_login'))


@csrf_exempt
def registrasi_label(request):
    nama = request.POST.get('name')
    email = request.POST.get('email')
    password = request.POST.get('password')
    kontak = request.POST.get('contact')
    
    idl = uuid4()
    id_phc = uuid4()



    query_str = f"INSERT INTO pemilik_hak_cipta VALUES ('{id_phc}', {int('3000')})"
    hasil = query(query_str)
    query_str = f"INSERT INTO label VALUES ('{idl}', '{email}', '{password}', '{nama}', '{kontak}', '{id_phc}')"
    hasil = query(query_str)

    if isinstance(hasil, int):
        pass
    else:
        #delete id_phc
        query_str = f"DELETE FROM pemilik_hak_cipta WHERE id = '{id_phc}'"
        return render(request, 'registrasi_label.html', {'error_message': 'Email sudah terdaftar.'})
    
    return HttpResponseRedirect(reverse('main:page_login'))


@csrf_exempt
def logout(request):
    request.session.flush()
    return HttpResponseRedirect(reverse('main:home'))


    


