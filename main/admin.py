# -*- encoding: utf-8 -*-

from django.contrib import admin
from main.models import *
from random import randint

class SpaAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('nombre',)}

class CirujanoAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('nombre',)}

admin.site.register(Spa,SpaAdmin)
admin.site.register(Cirujano,CirujanoAdmin)

# Register your models here.
