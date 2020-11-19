from unicodedata2 import normalize
from functools import partial

from django import forms
from django.forms import formset_factory

from .models import *

DatePicker = partial(forms.DateInput, {'class': 'datepicker'})

class AddService(forms.Form):

    service = forms.CharField(
        label = 'Prends ton service gars'
    )

    paiement = forms.CharField(
        label = 'Tu payes comment ?'
    )