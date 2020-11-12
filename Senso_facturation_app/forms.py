from unicodedata2 import normalize
from functools import partial

from django import forms

from .models import *

DatePicker = partial(forms.DateInput, {'class': 'datepicker'})