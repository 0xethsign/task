from django import forms
from django.contrib.auth.models import User
from django.forms.fields import CharField


class UploadFileForm(forms.Form):
    image = forms.ImageField()


class EditFileName(forms.Form):
    filename = CharField(max_length=200)
