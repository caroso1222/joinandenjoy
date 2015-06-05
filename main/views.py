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


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
csv_spas = BASE_DIR + "/csv-files/Clientes-SPA.csv"



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

	return render(request,'index.html',context)


def generate(request):
	context = {"enviado":"NO"}
	content = render_to_string('prueba.html', context) 
	content = smart_str(content)               

	with open(csv_spas,'rb') as csv_file:
		dialect = csv.Sniffer().sniff(csv_file.read().decode("latin1").encode('utf8'), delimiters=";")
		csv_file.seek(0)
		data_reader = csv.reader(csv_file.read().decode("latin1").encode('utf8').splitlines(), dialect)
		#data_reader = csv.reader(csv_file.read().decode("latin1").encode('utf8').splitlines())
		i = 0
		for row in data_reader:
			i = i+1
			try:
				if row[0]!='h1_arriba': # No se mete el primer registro
					h1_arriba = row[0].strip()
					h1_abajo = row[1].strip()
					h2 = row[2].strip()
					nombre = row[3].strip()
					telefono = row[4].strip()
					direccion = row[5].strip()
					ciudad = row[6].strip()
					email = row[7].strip()
					facebook = row[8].strip()
					contacto = row[9].strip()
					web = row[10].strip()
					nombre = nombre.replace (" ", "-")
					nombre = u'%s'%nombre
					#nombre = u"holaà"
					#nombre = (''.join((c for c in unicodedata.normalize('NFD', nombre) if unicodedata.category(c) != 'Mn'))).decode('unicode-escape')
					nombre = unicodedata.normalize('NFKD', nombre).encode('ascii','ignore')
					print nombre
			except Exception,err:
				print i
				print "error"
				print traceback.format_exc()
				break
	print "Spas actualizados"








	with open('prueba-2.html', 'w') as static_file:
		static_file.write(content)

	return render(request,'index.html',context)
