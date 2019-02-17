"""sorumvar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from sorumvaruygulama import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',views.Anasayfa,name="anasayfa"),
    url('veri_gun', views.veri_gun, name="veri_gun"),
    url(r'^(?P<kullaniciid>\d+)/veri_sil/$', views.veri_sil, name="veri_sil"),
      url(r'^(?P<soruid>\d+)/soru_gun/$', views.soru_gun, name="soru_gun"),
    url(r'^(?P<soruid>\d+)/soru_sil/$', views.soru_sil, name="soru_sil"),
    url('kayit_ekle', views.kayit_ekle),
    url('kayıtol/', views.Kayıtol,name="kayitol"),
    url('girisyap/', views.girisyap,name="girisyap"),
    url('giris_yap', views.Girisyap),
    url('veri_güncelle', views.veri_güncelle,name="veri_güncelle"),
    url('sorusor/', views.Soru,name="sorusor"),
    url('iletisim/$', views.iletisim, name="iletisim"),
    url('hesap/', views.hesap, name="hesap"),
    url('sorumvar', views.sorumvar),
    url(r'^(?P<id>\d+)/post/$',views.sorudetay ,name="sorudetay"),
    url(r'^(?P<id>\d+)/duyuru/$',views.duyurudetay,name='duyurudetay'),
    url('sifremiunuttum',views.sifremiunuttum,name="sifremiunuttum"),
    url('sifre_mail',views.sifre_mail,name="sifre_mail"),
    url('yeni_sifre', views.yeni_sifre, name="yeni_sifre"),
    url('sorular/',views.Sorular,name="sorular"),
    url('duyurular/',views.Duyurular,name='duyurular')
          ] +static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)