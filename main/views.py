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

# Create your views here.
def home(request):
	formulario = ContactenosForm(request.POST or None)
	if request.method == 'POST':
		if formulario.is_valid():
			nombre = formulario.cleaned_data['nombre']
			email = formulario.cleaned_data['email']
			mensaje = formulario.cleaned_data['mensaje']
			send_mail('Nuevo mensaje en hype.com.co', "Nombre: " + nombre + "\n" + "Email: " + email + "\n\n" + "Mensaje: " + "\n"+mensaje, 'holamundo@joinandenjoy.co',
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