from django.db import models
from django.urls import reverse
import  json
from urllib import request


header = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Basic Mjg1NmM5NzMtMDJjYS00MDY4LWFiODctYTRlZjc0ZTU3ZWEz"}


def onesignal(mesaj, url):
    payload = {"app_id": "3865b563-1d29-443d-a8da-7e6b459608c8", "included_segments": ["Active Users"], "contents": {"en": mesaj},  "url":url}
    request.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))

class kullanicilar(models.Model):
    isim=models.CharField(max_length=20)
    soyisim=models.CharField(max_length=20)
    kullaniciadi=models.CharField(max_length=20)
    parola=models.CharField(max_length=20)
    okul=models.CharField(max_length=50)
    sinif=models.CharField(max_length=100,null=True)
    numara=models.CharField(max_length=1000,null=True)
    kullanici_mail=models.EmailField(unique=True)
    soru_sayisi=models.IntegerField(default=0)

    class Meta:
        ordering=['-soru_sayisi','-id']


    def __str__(self):
        return self.isim

class sorular(models.Model):
    sorupuan=models.CharField(max_length=100,blank=True)
    kullanici_adi=models.CharField(max_length=50,blank=True)
    baslik=models.CharField(max_length=200)
    icerik=models.CharField(max_length=5000)
    ders=models.CharField(max_length=100)
    kitap=models.CharField(max_length=100,blank=True)
    sayfano=models.CharField(max_length=100,blank=True)
    soruno=models.CharField(max_length=100,blank=True)
    image=models.ImageField(null=True,blank=True)
    publishing_date=models.DateTimeField(auto_now_add=True)
    isim = models.CharField(max_length=50, blank=True)
    soyisim = models.CharField(max_length=50, blank=True)
    def __str__(self):
        return self.baslik

    def resim_görüntüle(self):
        return self.image.url

    def get_absolute_url(self):
        return reverse('sorudetay',kwargs={'id':self.id})

    class Meta:
        ordering=['-publishing_date']


class cevaplar(models.Model):
    kullaniciadi=models.CharField(max_length=20)
    cevap=models.CharField(max_length=200)
    sorunumarasi=models.IntegerField()
    publishing_date=models.DateTimeField(auto_now_add=True)
    cevapresmi=models.FileField(null=True,blank=True)
    isim = models.CharField(max_length=50, blank=True)
    soyisim = models.CharField(max_length=50, blank=True)
    def cevap_resim_görüntüle(self):
        return self.cevapresmi.url

    class Meta:
        ordering=['-publishing_date']

class duyurular(models.Model):
    isim=models.CharField(max_length=10)
    soyisim=models.CharField(max_length=15)
    baslik = models.CharField(max_length=100)
    duyuru=models.TextField(null=True)
    publishing_date=models.DateTimeField(auto_now_add=True)
    duyuru_sinif=models.CharField(max_length=50,null=True)
    resim=models.FileField(blank=True,null=True)


    def resim_görüntüle(self):
        return self.resim.url

    def get_absolute_url(self):
        return reverse('duyurudetay',kwargs={'id':self.id})

    class Meta:
        ordering=['-publishing_date']

    def __str__(self):
        return self.baslik

    def duyuru_resim_görüntüle(self):
        return self.resim.url

class puanlar(models.Model):
    puanidsi=models.IntegerField()
    puan=models.IntegerField(blank=True)

class mail_parola(models.Model):
    kullanici=models.CharField(max_length=50)
    parola=models.IntegerField()
    publishing_date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.kullanici