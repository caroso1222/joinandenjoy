# -*- encoding: utf-8 -*-
from django import forms

class ContactenosForm(forms.Form):
	nombre = forms.CharField(max_length = 100,
		widget=forms.TextInput(attrs={'class':'form-control simplebox', 'placeholder':'Tu nombre...'
			,'id':'nombre-input'}),
		required = False)

	email = forms.CharField(max_length = 100,
		widget=forms.TextInput(attrs={'class':'form-control simplebox', 'placeholder':'Tu email...'
			,'id':'email-input', 'type':'email'}),
		required = False)

	mensaje = forms.CharField(max_length = 1000,
		widget=forms.Textarea(attrs={'class':'form-control campo-mensaje', 'placeholder':'Déjanos tu mensaje...','rows':'5'
			,'id':'mensaje-input'}),
		required = False)