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

# formulaire avec des champs de facture
class PlageDateFacture(forms.ModelForm):

    class Meta:
        model = Facture
        fields = ['date_arrivee', 'date_depart']
        widgets = {
            'date_arrivee': DatePicker(),
            'date_depart': DatePicker()
        }

'''
class AddCulture(forms.Form):

    type_contenant = forms.ChoiceField(
        choices = TypeContenantCulturesChoix.choices,
        label = 'Type de contenant'
    )

    nom = forms.CharField(
        label = 'Nom (sans espace)'
    )

    question = forms.BooleanField(
        label = 'Souhaites-tu noter une rotation de culture ?',
        widget = forms.RadioSelect(
            choices = [
                ('Oui', 'Oui'),
                ('Non', 'Non')
            ],
            attrs = {'class': 'radio-check'}
        ),
        required = False
    )

    def __init__(self, *args, **kwargs):

        reponse = kwargs.pop('reponse')

        super(AddCulture, self).__init__(*args, **kwargs)

        if reponse == 'Oui':
            self.fields['phase'] = forms.ChoiceField(
                choices = PhaseCulturesChoix.choices,
                required = False,
            )

            self.fields['phase_date'] = forms.DateField(
                widget = DatePicker(),
                required = False
            )

class ActualiserCulture(forms.ModelForm):

    class Meta:
        model = PhaseCulture
        fields = ['phase', 'phase_date']
        labels = {
            'phase': PhaseCulture.phase.field.verbose_name,
            'phase_date': PhaseCulture.phase_date.field.verbose_name
        }
        widgets = {
            'phase': forms.RadioSelect(
                choices = PhaseCulturesChoix.choices,
                attrs = {'class': 'radio-check'}
            ),
            'phase_date': DatePicker()
        }
'''