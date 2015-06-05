from django.contrib import admin
from main.models import *
from random import randint

class SpaAdmin(admin.ModelAdmin):
	random_index = randint(0,999)
	prepopulated_fields = {'slug': ('nombre',)}

admin.site.register(Spa,SpaAdmin)

# Register your models here.
