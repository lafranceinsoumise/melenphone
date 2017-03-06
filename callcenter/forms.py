# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from django.contrib.admin import widgets
from django.contrib.auth.models import User
import requests
from django.conf import settings


class registerNewForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(),max_length=20,label="Nom d'utilisateur*")
    email=forms.EmailField(label="Email*")
    password1 = forms.CharField(widget=forms.PasswordInput(), label="Mot de passe*")
    password2 = forms.CharField(widget=forms.PasswordInput(), label ="Confirmation*")
    country = forms.CharField(widget=forms.TextInput(),max_length=50, label ="Pays*")
    city = forms.CharField(widget=forms.TextInput(),max_length=50, label ="Ville*")

    def clean_password2(self):
        password = self.cleaned_data.get('password1')
        passwordconfirm = self.cleaned_data.get('password2')
        if password and passwordconfirm:
            if (password != passwordconfirm):
                raise forms.ValidationError("Les mots de passe ne correspondent pas !")
            return passwordconfirm

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Cette adresse email est déjà utilisée !")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Trop tard ! Ce nom est déjà utilisé !")
        return username
