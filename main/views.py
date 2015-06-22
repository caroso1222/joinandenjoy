# -*- encoding: utf-8 -*-

from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from main.models import *
from django.template import RequestContext
from main.models import *
from forms import *
import datetime
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.utils.encoding import smart_str
import codecs
import traceback
import sys,os
import csv
import unicodedata
from random import randint
from django.core.mail import EmailMultiAlternatives
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from email.MIMEImage import MIMEImage


ENVIAR_A_FOUNDERS = "NO"
NUMERO_DE_PROPUESTAS = 430 #220

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
csv_spas = BASE_DIR + "/csv-files/Clientes-SPA.csv"
BASE_DIR_SPAS = BASE_DIR + "/main/templates/spas/"
csv_cirujanos = BASE_DIR + "/csv-files/Clientes-cirujanos.csv"
BASE_DIR_CIRUJANOS = BASE_DIR + "/main/templates/cirujanos/"


EMAIL_HOST = 'smtp.webfaction.com'
EMAIL_HOST_USER = 'sebastianmacias'
EMAIL_HOST_PASSWORD = 'Blogbotics123'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# Create your views here.
def home(request):
	formulario = ContactenosForm(request.POST or None)
	if request.method == 'POST':
		if formulario.is_valid():
			nombre = formulario.cleaned_data['nombre']
			email = formulario.cleaned_data['email']
			mensaje = formulario.cleaned_data['mensaje']
			send_mail('Nuevo mensaje en JoinAndEnjoy', "Nombre: " + nombre + "\n" + "Email: " + email + "\n\n" + "Mensaje: " + "\n"+mensaje, 'holamundo@joinandenjoy.co',
				['carlos.roso@joinandenjoy.co','sebastian.macias@joinandenjoy.co','holamundo@joinandenjoy.co'], fail_silently=False)
			request.session['mensaje_enviado'] = "SI"
			return HttpResponseRedirect('')
	try:
		if (request.session['mensaje_enviado'] == "SI"):
			context = {"enviado":"SI","formulario":formulario}
			request.session['mensaje_enviado'] = "NO"
		else:
			context = {"enviado":"NO","formulario":formulario}
	except:
		context = {"enviado":"NO","formulario":formulario}
		request.session['mensaje_enviado'] = "NO"
	for idx, cirujano in enumerate(Cirujano.objects.all()):
		#print "%d %s %s"%(idx, cirujano.nombre, cirujano.apellido)
		if idx < 350:
			cirujano.email = "SI"
			cirujano.save()

	return render(request,'index.html',context)

def ver_spa(request, slug):
	spa = get_object_or_404(Spa,slug = slug)
	h1_arriba = spa.h1_arriba
	h1_abajo = spa.h1_abajo
	h2 = spa.h2
	nombre = spa.nombre
	telefono = spa.telefono
	direccion = spa.direccion
	ciudad = spa.ciudad
	email = spa.email
	facebook = spa.facebook
	context = {"h1_arriba":h1_arriba,"h1_abajo":h1_abajo,"h2":h2,"nombre":nombre,"telefono":telefono,"direccion":direccion,"ciudad":ciudad,"email":email,"facebook":facebook}
	return render(request,'prueba.html', context)

def ver_cirujano(request, slug):
	cirujano = get_object_or_404(Cirujano,slug = slug)
	nombre = cirujano.nombre + " " + cirujano.apellido
	telefono = cirujano.telefono
	direccion = cirujano.direccion
	ciudad = cirujano.ciudad
	email = cirujano.email
	h2_arriba = cirujano.h2_arriba
	h2_abajo = cirujano.h2_abajo
	if request.method == 'POST':
		if request.POST['accion'] == 'EN':
			context = {"h2_arriba":h2_arriba,"h2_abajo":h2_abajo,"nombre":nombre,"telefono":telefono,"direccion":direccion,"ciudad":ciudad,"email":email,"idioma":"EN", "base":"base-cirujanos-en.html"}
		else:
			context = {"h2_arriba":h2_arriba,"h2_abajo":h2_abajo,"nombre":nombre,"telefono":telefono,"direccion":direccion,"ciudad":ciudad,"email":email,"idioma":"ES", "base":"base-cirujanos-es.html"}
	else:
		context = {"h2_arriba":h2_arriba,"h2_abajo":h2_abajo,"nombre":nombre,"telefono":telefono,"direccion":direccion,"ciudad":ciudad,"email":email,"idioma":"ES", "base":"base-cirujanos-es.html"}
	return render(request,'cirujano.html', context)

def generate_spa(request):
	with open(csv_spas,'rb') as csv_file:
		dialect = csv.Sniffer().sniff(csv_file.read().decode("latin1").encode('utf8'), delimiters=";")
		csv_file.seek(0)
		data_reader = csv.reader(csv_file.read().decode("latin1").encode('utf8').splitlines(), dialect)
		i = 0
		for row in data_reader:
			i = i+1
			try:
				if row[0]!='h1 arriba': # No se mete el primer registro
					spa, created = Spa.objects.get_or_create(nombre = row[3].strip())

					if created == True:
						#asigna los atributos a la nueva instancia del spa
						spa.h1_arriba = row[0].strip()
						spa.h1_abajo = row[1].strip()
						spa.h2 = row[2].strip()
						spa.nombre = row[3].strip()
						spa.telefono = row[4].strip()
						spa.direccion = row[5].strip()
						spa.ciudad = row[6].strip()
						spa.email = row[7].strip()
						spa.email2 = row[8].strip()
						spa.facebook = row[9].strip()
						spa.correo_enviado = "NO"
						#arma el contexto para pasarlo al template
						context = {"h1_arriba":spa.h1_arriba,"h1_abajo":spa.h1_abajo,"h2":spa.h2,"nombre":spa.nombre,"telefono":spa.telefono,"direccion":spa.direccion,"ciudad":spa.ciudad,"email":spa.email,"facebook":spa.facebook}
						#arma la url con guiones en vez de espacios, sin tildes y con un numero aleatorio
						la_url = spa.nombre.replace (" ", "-")
						la_url = la_url.replace (".", "-")
						la_url = la_url.replace ("&", "y")
						la_url = la_url.replace ("/", "-")
						la_url = smart_str(la_url).decode('utf-8')
						la_url = u'%s'%la_url
						la_url = unicodedata.normalize('NFKD', la_url).encode('ascii','ignore')
						random_index = randint(0,999)
						spa.slug = la_url + "-"+ "%d"%random_index
						#ingresa el spa a la base de datos
						spa.save()  
			except Exception,err:
				print i
				print "error"
				print traceback.format_exc()
				break
	print "Spas actualizados"
	context = {"h1_arriba":"h1_arriba"}
	return render(request,'index.html',context)

def emails_spa(request):

	for spa in Spa.objects.all():
		if spa.correo_enviado == "NO":
			spa.correo_enviado = "SI"
			spa.save()
			context = {"nombre":spa.nombre, "link":spa.slug, "h1":spa.h1_arriba}
			if spa.facebook != "NO":
				context = {"nombre":spa.nombre, "link":spa.slug, "h1":spa.h1_arriba, "tiene_fb":"SI", "fb_link":spa.facebook}
			html_content = render_to_string('spa-email.html', context)
			text_content = render_to_string('spa-email.txt', context)
			lista_correos = ['ce.roso398@gmail.com']
			if spa.email != "NO":
				lista_correos.append(spa.email)
				print "hoa"
			if spa.email2 != "NO":
				lista_correos.append(spa.email2)
				print "hoa"
			if spa.facebook != "NO":
				lista_correos.append('sebastian.macias.y@gmail.com')
			
			sujeto = spa.nombre + " - Desarrollo de pagina web"
			subject, from_email, to = unicodedata.normalize('NFKD', sujeto).encode('ascii','ignore'), 'sebastian.macias@joinandenjoy.co', lista_correos

			print lista_correos

			msg = EmailMultiAlternatives(subject, text_content, from_email, to)

			msg.attach_alternative(html_content, "text/html")
			msg.mixed_subtype = 'related'

			for f in ['Mock-up.jpg']:
				elpath = BASE_DIR + "/main/templates/static/img/Mock-up.jpg"
				fp = open(elpath,  'rb')
				msg_img = MIMEImage(fp.read())
				fp.close()
				msg_img.add_header('Content-ID', '<{}>'.format(f))
				msg.attach(msg_img)

			msg.send()

	context = {"h1_arriba":"h1_arriba"}
	return render(request,'index.html',context)

def emails_cirujano(request):
	i = 0
	for idx,cirujano in enumerate(Cirujano.objects.all()):
		if idx < NUMERO_DE_PROPUESTAS:
			if cirujano.correo_enviado == "NO":
				cirujano.correo_enviado = "SI"
				cirujano.save()
				nombre_entero = cirujano.nombre
				h1 = "Dr. " + cirujano.nombre
				context = {"nombre":cirujano.nombre, "link":cirujano.slug, "h1":h1}
				html_content = render_to_string('cirujano-email.html', context)
				text_content = render_to_string('cirujano-email.txt', context)
				lista_correos = []

				if ENVIAR_A_FOUNDERS == "SI":
					lista_correos = ['ce.roso398@gmail.com','sebastian.macias.y@gmail.com']
				else:
					lista_correos = ['sebastian.macias@joinandenjoy.co']

				if cirujano.email != "NO":
					lista_correos.append(cirujano.email)
				
				sujeto = "Desarrollo de website del cirujano " + cirujano.nombre
				subject, from_email, to = unicodedata.normalize('NFKD', sujeto).encode('ascii','ignore'), 'carlos.roso@joinandenjoy.co', lista_correos

				print lista_correos

				msg = EmailMultiAlternatives(subject, text_content, from_email, to)

				msg.attach_alternative(html_content, "text/html")
				msg.mixed_subtype = 'related'

				for f in ['Mock-up.jpg']:
					elpath = BASE_DIR + "/main/templates/static/img/Mock-up-medico.jpg"
					fp = open(elpath,  'rb')
					msg_img = MIMEImage(fp.read())
					fp.close()
					msg_img.add_header('Content-ID', '<{}>'.format(f))
					msg.attach(msg_img)

				msg.send()

	context = {"h1_arriba":"h1_arriba"}
	return render(request,'index.html',context)

def generate_cirujano(request):
	filename = csv_cirujanos
	reader = unicode_csv_reader(open(filename))
	for row in reader:
		if row[0]!='nombre':
			cirujano, created = Cirujano.objects.get_or_create(nombre = row[0].strip(), apellido = row[2].strip())
			if created == True:
				#asigna los atributos a la nueva instancia del spa
				cirujano.nombre = row[0].strip()
				cirujano.direccion = row[1].strip()
				#apellido = smart_str(row[2].strip()).decode('utf-8')
				#la_url = unicodedata.normalize('NFKD', apellido).encode('ascii','ignore')
				cirujano.apellido = row[2].strip()
				nombre_entero = cirujano.nombre + " " + cirujano.apellido
				cirujano.ciudad = row[3].strip()
				cirujano.telefono = row[4].strip()
				cirujano.email = row[7].strip()
				cirujano.h2_arriba = nombre_entero
				cirujano.h2_abajo = "NO"
				cirujano.correo_enviado = "NO"
				#arma el contexto para pasarlo al template
				
				context = {"h2_arriba":cirujano.h2_arriba,"h2_abajo":cirujano.h2_abajo,"nombres":nombre_entero,"telefono":cirujano.telefono,"direccion":cirujano.direccion,"ciudad":cirujano.ciudad,"email":cirujano.email}
				#arma la url con guiones en vez de espacios, sin tildes y con un numero aleatorio
				la_url = nombre_entero.replace (" ", "-")
				la_url = la_url.replace (".", "-")
				la_url = la_url.replace ("&", "y")
				la_url = la_url.replace ("/", "-")
				la_url = smart_str(la_url).decode('utf-8')
				la_url = u'%s'%la_url
				la_url = unicodedata.normalize('NFKD', la_url).encode('ascii','ignore')
				random_index = randint(0,9999)
				la_url = la_url.lower()
				cirujano.slug = la_url + "-"+ "%d"%random_index
				#ingresa el spa a la base de datos
				cirujano.save()  
	
	print "Cirujanos actualizados"
	context = {"h1_arriba":"h1_arriba"}
	return render(request,'index.html',context)

def unicode_csv_reader(utf8_data, dialect=csv.excel, **kwargs):
    csv_reader = csv.reader(utf8_data, dialect=dialect, **kwargs)
    for row in csv_reader:
        yield [unicode(cell, 'utf-8') for cell in row]
