from django.shortcuts import render,HttpResponse
from django.db.models import Max
from .models import *
from django.contrib import messages
import smtplib
import random
from smtplib import SMTPRecipientsRefused
from django.core.mail import send_mail
from datetime import datetime, timezone
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

def Anasayfa(request):
    soru_puanlari = []

    if "kullanici_cerezi" in request.COOKIES:
        duyuru = duyurular.objects.all()[0]
        soru = sorular.objects.all()[0]
        puan_soru=sorular.objects.all()
        for i in puan_soru:
            soru_puanlari.append(i.sorupuan)

        soru_puanlari.sort()
        max_puan=soru_puanlari[-1]
        max_puan_soru=sorular.objects.filter(sorupuan=max_puan)
        soru_sayısı=sorular.objects.filter().count()
        kullanicisorulari=kullanicilar.objects.all()
        return render(request, "anasayfa.html",
                      {'duyuru': duyuru, 'soru': soru, 'max_puan_soru': max_puan_soru,'soru_sayısı':soru_sayısı,'kullanicisorulari':kullanicisorulari})

    else:
        messages.success(request,'Öncelikle giriş yapmalısınız.')
        return render(request,'girisyap.html')

    soru_puanlari.clear()


def duyurudetay(request,id):
    duyuru=duyurular.objects.get(id=id)
    return render(request,'duyurudetay.html',{'duyuru':duyuru})


def Duyurular(request):
    if "kullanici_cerezi" in request.COOKIES:
        duyuru = duyurular.objects.all()

        return render(request,"duyurular.html",{'duyurular':duyuru})
    else:
        return render(request,'girisyap.html')


def veri_gun(request):
    kullaniciadi=request.session['bilgiler']
    kullanici=kullanicilar.objects.get(kullaniciadi=kullaniciadi)
    kullanici_sinif=kullanici.sinif
    return render(request,'veri_güncelle.html',{'sinif':kullanici_sinif})

def soru_sil(request,soruid):
    soru=sorular.objects.get(id=soruid)
    soru.delete()

    duyuru = duyurular.objects.all()[0]
    kullaniciadi = request.session['bilgiler']
    kullanici = kullanicilar.objects.get(kullaniciadi=kullaniciadi)
    soru = sorular.objects.filter(kullanici_adi=kullaniciadi)
    soru_sayisi=kullanici.soru_sayisi
    soru_sayisi-=1
    kullanici.soru_sayisi=soru_sayisi
    kullanici.save()
    messages.success(request,'Başarıyla silindi.')
    return render(request, "hesap.html", {'kullanici': kullanici, 'soru': soru, 'duyuru': duyuru})
def soru_gun(request,soruid):
    if request.method=="POST":
        baslik = request.POST.get('baslik')
        icerik = request.POST.get('icerik')
        ders = request.POST.get('ders')
        kitap = request.POST.get('kitap')
        sayfano = request.POST.get('sayfano')
        soruno = request.POST.get('soruno')
        resim = request.FILES.get('resim')
        if baslik:
            sorudeger=sorular.objects.get(id=soruid)
            sorudeger.baslik=baslik
            sorudeger.save()
        if icerik:
            sorudeger=sorular.objects.get(id=soruid)
            sorudeger.icerik=icerik
            sorudeger.save()
        if ders:
            sorudeger=sorular.objects.get(id=soruid)
            sorudeger.ders=ders
            sorudeger.save()
        if kitap:
            sorudeger=sorular.objects.get(id=soruid)
            sorudeger.kitap=kitap
            sorudeger.save()
        if sayfano:
            sorudeger=sorular.objects.get(id=soruid)
            sorudeger.sayfano=sayfano
            sorudeger.save()
        if soruno:
            sorudeger=sorular.objects.get(id=soruid)
            sorudeger.soruno=soruno
            sorudeger.save()
        if resim:
            sorudeger=sorular.objects.get(id=soruid)
            sorudeger.resim=resim
            sorudeger.save()
        duyuru = duyurular.objects.all()[0]
        kullaniciadi = request.session['bilgiler']
        kullanici = kullanicilar.objects.get(kullaniciadi=kullaniciadi)
        soru = sorular.objects.filter(kullanici_adi=kullaniciadi)
        messages.success(request,'Başarıyla güncellendi.')
        return render(request, "hesap.html", {'kullanici': kullanici, 'soru': soru, 'duyuru': duyuru})
    else:
        soru=sorular.objects.get(id=soruid)
        return render(request,'sorugüncelle.html',{'soru':soru})

def veri_güncelle(request):
    if request.method == "POST":
        #formdan verilerin alındığı satırlar
        isim = request.POST.get('isim')
        soyisim = request.POST.get('soyisim')
        kullaniciadi_form = request.POST.get('kullaniciadi')
        parola = request.POST.get('parola')
        okul = request.POST.get('okul')
        sinif = request.POST.get('sinif')
        numara = request.POST.get('numara')
        kullanici_mail = request.POST.get('mail')
        kullaniciadi = request.session['bilgiler']
        if isim:
            kullanici=kullanicilar.objects.get(kullaniciadi=kullaniciadi)
            kullanici.isim=isim
            kullanici.save()

        if soyisim:
            kullanici =kullanicilar.objects.get(kullaniciadi=kullaniciadi)
            kullanici.soyisim = soyisim
            kullanici.save()
        if kullaniciadi_form:
            kullanicivarmi=kullanicilar.objects.filter(kullaniciadi=kullaniciadi_form)
            if kullanicivarmi:
                messages.success(request,'Bu kullanıcı adı kullanılıyor.')
                kullaniciadi = request.session['bilgiler']
                kullanici = kullanicilar.objects.get(kullaniciadi=kullaniciadi)
                kullanici_sinif = kullanici.sinif
                return render(request, 'veri_güncelle.html', {'sinif': kullanici_sinif})
            else:
                kullanici = kullanicilar.objects.get(kullaniciadi=kullaniciadi)
                soru_kullaniciadi = sorular.objects.filter(kullanici_adi=kullaniciadi)
                cevap_kullaniciadi = cevaplar.objects.filter(kullaniciadi=kullaniciadi)
                kullanici.kullaniciadi = kullaniciadi_form
                if cevap_kullaniciadi:
                    for i in cevap_kullaniciadi:
                        i.kullaniciadi = kullaniciadi_form
                        i.save()
                if soru_kullaniciadi:
                    for i in soru_kullaniciadi:
                        i.kullanici_adi = kullaniciadi_form
                        i.save()
                yenikullaniciadi = kullanici.kullaniciadi
                request.session['bilgiler'] = yenikullaniciadi
                kullanici.save()

        if parola:
            kullaniciadi = request.session['bilgiler']
            kullanici =kullanicilar.objects.get(kullaniciadi=kullaniciadi)
            kullanici.parola = parola
            kullanici.save()
        if okul:
            kullaniciadi = request.session['bilgiler']
            kullanici =kullanicilar.objects.get(kullaniciadi=kullaniciadi)
            kullanici.okul = okul
            kullanici.save()
        if sinif:
            kullaniciadi = request.session['bilgiler']
            kullanici =kullanicilar.objects.get(kullaniciadi=kullaniciadi)
            kullanici.sinif = sinif
            kullanici.save()
        if numara:
            kullaniciadi = request.session['bilgiler']
            kullanici =kullanicilar.objects.get(kullaniciadi=kullaniciadi)
            kullanici.numara = numara
            kullanici.save()
        if kullanici_mail:
            kullaniciadi = request.session['bilgiler']
            kullanici =kullanicilar.objects.get(kullaniciadi=kullaniciadi)
            kullanici.kullanici_mail = kullanici_mail
            kullanici.save()
    soru_puanlari = []

    if "kullanici_cerezi" in request.COOKIES:
        duyuru = duyurular.objects.all()[0]
        soru = sorular.objects.all()[0]
        puan_soru = sorular.objects.all()
        for i in puan_soru:
            soru_puanlari.append(i.sorupuan)

        soru_puanlari.sort()
        max_puan = soru_puanlari[-1]
        max_puan_soru = sorular.objects.filter(sorupuan=max_puan)
        soru_sayısı = sorular.objects.filter().count()
        kullanicisorulari = kullanicilar.objects.all()
        return render(request, "anasayfa.html",
                      {'duyuru': duyuru, 'soru': soru, 'max_puan_soru': max_puan_soru, 'soru_sayısı': soru_sayısı,
                       'kullanicisorulari': kullanicisorulari})


def sifremiunuttum(request):
    return render(request,'sifredegistir.html')

def sifre_mail(request):
    if request.method=="POST":
        kullaniciisim=request.POST.get('kullaniciadi')
        kullanicimail=request.POST.get('mail')
        kullanici_filtre=kullanicilar.objects.filter(kullaniciadi=kullaniciisim,kullanici_mail=kullanicimail)
        if kullanici_filtre:
            parola_varmi=mail_parola.objects.filter(kullanici=kullaniciisim)

            if parola_varmi:
                eski_parola=mail_parola.objects.get(kullanici=kullaniciisim)
                eski_parola_zaman=eski_parola.publishing_date
                güncel_zaman=datetime.now(timezone.utc)
                zaman_fark=güncel_zaman-eski_parola_zaman
                if zaman_fark.days>0:
                    eski_parola.delete()
                else:
                    if zaman_fark.seconds>300:
                        eski_parola.delete()
                    else:
                        messages.success(request, 'parola gönderilmiş ikinci kez parola almadan önce 5 dk bekleyin.')
                        return render(request, 'girisyap.html')
            parola_deger=mail_parola.objects.filter(kullanici=kullaniciisim)
            if not parola_deger:
                rast_sayi = random.randint(100, 1000)
                yeni_parola=mail_parola(
                    parola=rast_sayi,
                    kullanici=kullaniciisim
                )
                yeni_parola.save()

                parola_deger=mail_parola.objects.get(kullanici=kullaniciisim)
                send_mail('Şifre değiştirme işlemi',
                          'Şifrenizi değiştirmek için bu parolayı kullanın:{}'.format(parola_deger.parola),
                          'mnsbyesor@gmail.com',
                          [kullanicimail],
                          fail_silently=False,
                          )
                messages.success(request, "Mail adresinizi kontrol edin ve bu işlem için oradaki parolayı kullanın.")
                return render(request, "yenisifre.html")
        else:
            messages.success(request,'Kullanıcı adı ve şifreniz kayıtlı değil.Lütfen tekrar deneyin.')
            return render(request,'girisyap.html')
    else:
        return render(request, 'girisyap.html')

def yeni_sifre(request):
    if request.method=="POST":
        kullaniciadi=request.POST.get('kullaniciadi')
        parola=request.POST.get('parola')
        yenisifre=request.POST.get('yenisifre')
        parola_deger = mail_parola.objects.filter(kullanici=kullaniciadi,parola=parola)
        if parola_deger:
            kullanici=kullanicilar.objects.get(kullaniciadi=kullaniciadi)
            kullanici.parola=yenisifre
            kullanici.save()
            messages.success(request,'Şifre değiştirme başarılı.')
            return render(request,'girisyap.html')
        else:
            messages.success(request,'Bu şifre geçersiz')
            return render(request,'girisyap.html')




def hesap(request):
    if "kullanici_cerezi" in request.COOKIES:
        duyuru = duyurular.objects.all()[0]
        kullaniciadi=request.session['bilgiler']
        kullanici = kullanicilar.objects.get(kullaniciadi=kullaniciadi)
        soru = sorular.objects.filter(kullanici_adi=kullaniciadi)
        soru_sayısı=sorular.objects.filter(kullanici_adi=kullaniciadi).count()

        return render(request, "hesap.html",{'kullanici':kullanici, 'soru': soru,'duyuru':duyuru,'soru_sayısı':soru_sayısı})
    else:
        messages.success(request,"Öncelikle giriş yapın.")
        return render(request,"girisyap.html")

def Kayıtol(request):
    return render(request,"kayıtol.html")

def girisyap(request):
    if "kullanici_cerezi" in request.COOKIES:
        messages.success(request,"Zaten giriş yapılmış.")
        soru_puanlari = []

        if "kullanici_cerezi" in request.COOKIES:
            duyuru = duyurular.objects.all()[0]
            soru = sorular.objects.all()[0]
            puan_soru = sorular.objects.all()
            for i in puan_soru:
                soru_puanlari.append(i.sorupuan)

            soru_puanlari.sort()
            max_puan = soru_puanlari[-1]
            max_puan_soru = sorular.objects.filter(sorupuan=max_puan)
            soru_sayısı = sorular.objects.filter().count()
            kullanicisorulari = kullanicilar.objects.all()
            return render(request, "anasayfa.html",
                          {'duyuru': duyuru, 'soru': soru, 'max_puan_soru': max_puan_soru, 'soru_sayısı': soru_sayısı,
                           'kullanicisorulari': kullanicisorulari})

    else:
        return render(request,"girisyap.html")

def iletisim(request):
    if "kullanici_cerezi" in request.COOKIES:
        duyuru = duyurular.objects.all()[0]

        return render(request, "iletisimHakkinda.html", {'duyuru': duyuru})
    else:
        return render(request,"girisyap.html")


def kayit_ekle(request):
    if request.method=="POST":
        #formdan verilerin alındığı satırlar
        isim=request.POST.get('isim')
        soyisim=request.POST.get('soyisim')
        kullaniciadi=request.POST.get('kullaniciadi')
        parola=request.POST.get('parola')
        okul=request.POST.get('okul')
        sinif=request.POST.get('sinif')
        numara=request.POST.get('numara')
        kullanici_mail=request.POST.get('mail')


        #hatalar isminde bir dizi ye if yapıları ile yapılan kontroller ile gerekli koşulları sağlanmasını sağlayan hataları yazdık.
        hatalar=[]
        sayilar=["0","1","2","3","4","5","6","7","8","9"]
        if not (isim and soyisim):
            hatalar.append("İsim veya Soyisim kısımları boş kalmamalı.")
        if not (kullaniciadi and parola):
            hatalar.append("Kullanici adi veya parola kısımları boş kalmamalı.")
        if not (okul):
            hatalar.append("Okul kısmı boş kalmamalı.")
        if not (sinif and numara):
            hatalar.append("Sınıf veya numara kısımları boş kalmamalı.")

        if not (kullanici_mail):
            hatalar.append("Mail kısmı boş kalmamalı.")

        for i in numara:
            if not i in sayilar:
                hatalar.append("Numara da sadece sayı kullanmalısınız.")

        kullaniciadi_vt=kullanicilar.objects.filter(kullaniciadi=kullaniciadi)
        if kullaniciadi_vt:
            hatalar.append("Bu kullanıcı adı kullanılıyor.Başka bir kullanıcı adı bulmanız gerek.")

        #veri tabanına kayıt yapıldı.
        kayit=kullanicilar(
        isim=isim,
        soyisim=soyisim,
        kullaniciadi=kullaniciadi,
        parola=parola,
        okul=okul,
        sinif=sinif,
        numara=numara,
        kullanici_mail=kullanici_mail)
        if len(hatalar) == 0 :
            kayit.save()
            messages.success(request,"Başarılı bir şekilde kayıt oluşturdunuz.")

            return render(request,"girisyap.html")
        else:
            return render(request,"kayıtol.html",{'hatalar':hatalar})





def Girisyap(request):
    soru_puanlari=[]
    if request.method=="POST":
        kullaniciadi=request.POST.get('kullaniciadi')
        parola=request.POST.get('parola')

        girishataları=[]
        giris=[]
        bilgi=[]
        if not (kullaniciadi and parola):
            girishataları.append("Kullanıcı adı ya da parola boş kalamaz.")

        kullanici_isim=kullanicilar.objects.filter(kullaniciadi=kullaniciadi)
        if kullanici_isim:
            Girisfiltre=kullanicilar.objects.filter(kullaniciadi=kullaniciadi,parola=parola)
            if Girisfiltre:
                duyuru = duyurular.objects.all()[0]
                soru = sorular.objects.all()[0]
                puan_soru = sorular.objects.all()
                for i in puan_soru:
                    soru_puanlari.append(i.sorupuan)

                soru_puanlari.sort()
                max_puan = soru_puanlari[-1]
                max_puan_soru = sorular.objects.filter(sorupuan=max_puan)
                soru_sayısı = sorular.objects.filter().count()
                kullanicisorulari = kullanicilar.objects.all()

                messages.success(request, "Giriş başarılı.")

                if "kullanici_cerezi" in request.COOKIES:
                    return render(request, 'anasayfa.html')

                else:
                    bilgi.append(kullaniciadi)
                    bilgi.append(parola)
                    response=render(request, "anasayfa.html",
                              {'duyuru': duyuru, 'soru': soru, 'max_puan_soru': max_puan_soru,
                               'soru_sayısı': soru_sayısı, 'kullanicisorulari': kullanicisorulari})
                    response.set_cookie('kullanici_cerezi',kullaniciadi)
                    request.session['bilgiler']=kullaniciadi
                    return response
            else:
                girishataları.append("Kullanıcı adı ve şifre eşleşmedi.")

        else:
            girishataları.append("Böyle bir kullanıcı bulunamadı.")

        if len(girishataları)>0:
            return render(request,"girisyap.html",{'girishataları':girishataları})

def Soru(request):
    if "kullanici_cerezi" in request.COOKIES:
        duyuru = duyurular.objects.all()[0]
        return render(request,'sorusor.html',{'duyuru':duyuru})
    else:
        return render(request,'girisyap.html')

def sorumvar(request):

        if request.method=="POST":
            kullanici_adi=request.session['bilgiler']
            baslik=request.POST.get('baslik')
            icerik=request.POST.get('icerik')
            ders=request.POST.get('ders')
            kitap=request.POST.get('kitap')
            sayfano=request.POST.get('sayfano')
            soruno=request.POST.get('soruno')
            resim=request.FILES.get('resim')
            kullanici=kullanicilar.objects.get(kullaniciadi=kullanici_adi)
            isim=kullanici.isim
            soyisim=kullanici.soyisim
            soru_sayisi=kullanici.soru_sayisi
            if not baslik:
                messages.success(request,"Lütfen bir başlık girin")
                return render(request, 'sorusor.html')
            else:
                soru_sayisi+=1
                kullanici.soru_sayisi=soru_sayisi
                kullanici.save()
                kayit = sorular(baslik=baslik, icerik=icerik, ders=ders, image=resim, kitap=kitap, sayfano=sayfano,
                                soruno=soruno, kullanici_adi=kullanici_adi,isim=isim,soyisim=soyisim)
                kayit.save()
                messages.success(request, "Başarılı bir şekilde soru oluşturdunuz.")
                soru_list = sorular.objects.all()
                paginator = Paginator(soru_list, 5)
                page = request.GET.get('sayfa')
                try:
                    soru = paginator.page(page)
                except PageNotAnInteger:
                    soru = paginator.page(1)
                except EmptyPage:
                    soru = paginator.page(paginator.num_pages)

                duyuru = duyurular.objects.all()[0]
                return render(request, 'sorular.html', {'soru': soru, 'duyuru': duyuru})


def sorudetay(request,id):
    sorunumarasi = id

    if request.method == "POST":
        kullaniciadi = request.session['bilgiler']
        kullanici = kullanicilar.objects.get(kullaniciadi=kullaniciadi)
        isim = kullanici.isim
        soyisim = kullanici.soyisim
        cevap = request.POST.get('cevap')
        cevapresmi = request.FILES.get('resim')
        kayit = cevaplar(kullaniciadi=kullaniciadi, cevap=cevap, sorunumarasi=sorunumarasi, cevapresmi=cevapresmi,isim=isim,soyisim=soyisim)
        kayit.save()
        if "kullanici_cerezi" in request.COOKIES:
            duyuru = duyurular.objects.all()[0]
            bilgi = request.session['bilgiler']
            soru = sorular.objects.get(id=id)
            cevap = cevaplar.objects.filter(sorunumarasi=id)
            return render(request, 'detay.html', {'soru': soru, 'cevap': cevap,'duyuru':duyuru})
        else:
            return render(request, 'girisyap.html')

    if request.method == "GET":
        puantoplam = 0
        puan = request.GET.get('puan')
        if puan:
            puankayit = puanlar(puan=puan, puanidsi=id)
            puankayit.save()
        sorupuanlari = puanlar.objects.filter(puanidsi=id)
        if sorupuanlari:
            for i in sorupuanlari:
                puantoplam += int(i.puan)
            Puanuzunluk = len(sorupuanlari)
            Ortpuan = puantoplam / Puanuzunluk
            soru = sorular.objects.get(id=id)
            soru.sorupuan = Ortpuan
            soru.save()

        if "kullanici_cerezi" in request.COOKIES:
            duyuru = duyurular.objects.all()[0]
            bilgi = request.session['bilgiler']
            soru = sorular.objects.get(id=id)
            cevap = cevaplar.objects.filter(sorunumarasi=id)
            return render(request, 'detay.html', {'soru': soru, 'cevap': cevap,'duyuru':duyuru})
        else:
            return render(request, 'girisyap.html')



    if "kullanici_cerezi" in request.COOKIES:
        duyuru = duyurular.objects.all()[0]
        bilgi = request.session['bilgiler']
        soru = sorular.objects.get(id=id)
        cevap = cevaplar.objects.filter(sorunumarasi=id)
        return render(request, 'detay.html',{'soru':soru,'cevap':cevap,'duyuru':duyuru})
    else:
        return render(request, 'girisyap.html')

def veri_sil(request,kullaniciid):
    kullanici=kullanicilar.objects.get(id=kullaniciid)
    kullanici.delete()

    response = render(request, "girisyap.html",)
    response.delete_cookie('kullanici_cerezi')

    return response

def Sorular(request):
    if "kullanici_cerezi" in request.COOKIES:
        soru_list = sorular.objects.all()
        paginator = Paginator(soru_list, 5)
        page = request.GET.get('sayfa')
        try:
            soru = paginator.page(page)
        except PageNotAnInteger:
            soru = paginator.page(1)
        except EmptyPage:
            soru = paginator.page(paginator.num_pages)

        duyuru = duyurular.objects.all()[0]
        return render(request, 'sorular.html', {'soru': soru, 'duyuru': duyuru})
    else:
        return render(request,'girisyap.html')