from django.contrib import admin
from .models import *

admin.site.register(kullanicilar)
admin.site.register(sorular)
admin.site.register(cevaplar)
admin.site.register(duyurular)
admin.site.register(puanlar)