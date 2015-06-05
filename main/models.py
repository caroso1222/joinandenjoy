from django.db import models
from django.db.models import permalink
# Create your models here.

class Spa(models.Model):
	nombre = models.CharField(max_length = 200)
	telefono = models.CharField(max_length = 200)
	direccion = models.CharField(max_length = 200)
	ciudad = models.CharField(max_length = 200)
	email = models.CharField(max_length = 200)
	email2 = models.CharField(max_length = 200)
	facebook = models.CharField(max_length = 200)
	h1_arriba = models.CharField(max_length = 200)
	h1_abajo = models.CharField(max_length = 200)
	h2 = models.CharField(max_length = 200)
	correo_enviado = models.CharField(max_length = 20)
	slug = models.SlugField(max_length = 100, unique = True)

	def __unicode__(self):
		return '%s'%self.nombre

	@permalink
	def get_absolute_url(self):
		return ('view_blog_post',None,{'slug':self.slug})
